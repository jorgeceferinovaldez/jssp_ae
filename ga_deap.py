import os
import random
import numpy
import pandas as pd
import multiprocessing
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from deap import base, creator, tools, algorithms
from typing import List, Tuple
import traceback

#Introduction Genetic Algorithm

# Basic Description Genetic algorithms are inspired by Darwin's theory about evolution. Solution to a problem solved by genetic algorithms is evolved.

# Algorithm is started with a set of solutions (represented by chromosomes) called population. Solutions from one population are taken and used to form a new population. This is motivated by a hope, that the new population will be better than the old one. Solutions which are selected to form new solutions (offspring) are selected according to their fitness - the more suitable they are the more chances they have to reproduce.

# Outline of the Basic Genetic Algorithm

#     [Start] Generate random population of n chromosomes (suitable solutions for the problem)
#     [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
#     [New population] Create a new population by repeating following steps until the new population is complete
#     [Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
#      [Crossover] With a crossover probability cross over the parents to form a new offspring (children). If no crossover was performed, offspring is an exact copy of parents.
#     [Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
#     [Accepting] Place new offspring in a new population
#     [Replace] Use new generated population for a further run of algorithm
#     [Test] If the end condition is satisfied, stop, and return the best solution in current population
#     [Loop] Go to step 2


class JSSP_Instance:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.n_jobs = 0
        self.n_machines = 0
        self.processing_times = None
        self.machine_sequence = None
        self.load_instance()

    def load_instance(self):
        try:
            with open(self.file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                self.best_value = int(lines[0])
                self.second_value = int(lines[1])
                self.data = [list(map(int, line.split())) for line in lines[2:]]
                self.n_jobs = len(self.data)
                # Find the maximum machine index in all jobs
                max_machine_index = 0
                for row in self.data:
                    machine_indices = row[::2]
                    if machine_indices:
                        max_machine_index = max(max_machine_index, max(machine_indices))
                self.n_machines = max_machine_index + 1
                # Build machine_sequence and processing_times
                self.machine_sequence = np.zeros((self.n_jobs, len(self.data[0]) // 2), dtype=int)
                self.processing_times = np.zeros((self.n_jobs, len(self.data[0]) // 2))
                for i, row in enumerate(self.data):
                    for j in range(len(row) // 2):
                        self.machine_sequence[i][j] = row[j*2]
                        self.processing_times[i][j] = row[j*2+1]
                print(f"Loaded: jobs={self.n_jobs}, machines={self.n_machines}")
        except Exception as e:
            print(f"Exception in load_instance: {e}")
            raise Exception(f"Error loading instance file: {str(e)}")


class JSSP_DEAP:
    def __init__(self, instance: JSSP_Instance):
        self.instance = instance
        self.n_jobs = instance.n_jobs
        self.n_machines = instance.n_machines
        self.toolbox = base.Toolbox()
        self.setup_toolbox()

    def setup_toolbox(self):
        """Set up the DEAP genetic algorithm toolbox"""
        # Create fitness and individual classes
        if self.n_jobs < 1:
            raise ValueError("Instance must have at least one job.")
        
        # Clear any existing definitions
        if hasattr(creator, "FitnessMin"):
            del creator.FitnessMin
        if hasattr(creator, "Individual"):
            del creator.Individual
        
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        
        # Use 0-based job indices for crossover compatibility
        job_ids = list(range(self.n_jobs))
        self.toolbox.register("indices", random.sample, job_ids, self.n_jobs)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate_schedule)
        self.toolbox.register("mate", tools.cxOrdered)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        
    def run(self, pop_size, n_gen, cx_pb=0.7, mut_pb=0.2):
        """Run the genetic algorithm"""
        # Initialize population
        pop = self.toolbox.population(n=pop_size)
        print(pop)
        hof = tools.HallOfFame(1)
        
        # Statistics setup
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        # Run algorithm
        pop, logbook = algorithms.eaSimple(
            pop, 
            self.toolbox, 
            cxpb=cx_pb,
            mutpb=mut_pb, 
            ngen=n_gen,
            stats=stats,
            halloffame=hof,
            verbose=True
        )
        
        return pop, logbook, hof

    def evaluate_schedule(self, individual: List[int]) -> Tuple[float,]:
        """Calculate makespan for a job sequence using instance data"""
        # Initialize machine completion times and job progress
        machine_times = [0] * self.n_machines
        job_progress = [0] * self.n_jobs
        
        # For each operation in the sequence
        for job_id in individual:
            job = job_id  # job_id is already 0-based
            
            if job_progress[job] >= self.n_machines:
                continue
                
            current_step = job_progress[job]
            machine = self.instance.machine_sequence[job][current_step]
            processing_time = self.instance.processing_times[job][current_step]
            
            # Calculate earliest possible start time
            if current_step > 0:
                prev_machine = self.instance.machine_sequence[job][current_step - 1]
                earliest_start = max(machine_times[machine], machine_times[prev_machine])
            else:
                earliest_start = machine_times[machine]
            
            # Update machine time and job progress
            machine_times[machine] = earliest_start + processing_time
            job_progress[job] += 1
        
        return max(machine_times),


def main():
    try:
        # Get list of instance files
        current_dir = os.getcwd()
        
        # Get the instances files
        instance_dir = os.path.join(current_dir, 'instancias')
        instance_files = [f for f in os.listdir(instance_dir) if f.endswith('.txt')]
        print("These are the instance files", instance_files)
        if not instance_files:
            print(f"ERROR: No .txt files found in {instance_dir}")
            return
        
        results = []
        
        for instance_file in instance_files:
            print(f"\nProcessing instance: {instance_file}")
            
            # Load instance
            instance_path = os.path.join(instance_dir, instance_file)
            instance = JSSP_Instance(instance_path)
            print(f"Loaded instance: jobs={instance.n_jobs}, machines={instance.n_machines}")

            # Initialize and run GA
            jssp = JSSP_DEAP(instance)
            pop, log, hof = jssp.run(
                pop_size=10,
                n_gen=5,
                cx_pb=0.65,
                mut_pb=0.05
            )

            print(pop)

            # Store results
            best = hof[0]
            makespan = jssp.evaluate_schedule(best)[0]
            
            results.append({
                'instance': instance_file,
                'makespan': makespan,
                'best_sequence': list(best),
                'generations': len(log)
            })

            # Plot evolution for this instance
            gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
            plt.figure(figsize=(10, 6))
            plt.plot(gen, min_, "g-", label="Minimum")
            plt.plot(gen, avg, "r-", label="Average")
            plt.plot(gen, max_, "b-", label="Maximum")
            plt.xlabel("Generation")
            plt.ylabel("Makespan")
            plt.title(f"Evolution of Fitness - Instance {instance_file}")
            plt.legend()
            plt.savefig(f"evolution_{instance_file}.png")
            plt.close()

        # Save results to file
        results_df = pd.DataFrame(results)
        results_df.to_csv('jssp_results.csv', index=False)
        
        # Print summary
        print("\n=== Final Results ===")
        for result in results:
            print(f"\nInstance: {result['instance']}")
            print(f"Makespan: {result['makespan']:.2f}")
            print(f"Best sequence: {result['best_sequence']}")

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
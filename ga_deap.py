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



# Introduction Genetic Algorithm

# Basic Description Genetic algorithms are inspired by Darwin's theory about evolution. Solution to a problem solved by genetic algorithms is evolved.

# Algorithm is started with a set of solutions (represented by chromosomes) called population. Solutions from one population are taken and used to form a new population. This is motivated by a hope, that the new population will be better than the old one. Solutions which are selected to form new solutions (offspring) are selected according to their fitness - the more suitable they are the more chances they have to reproduce.

# Outline of the Basic Genetic Algorithm

#     [Start] Generate random population of n chromosomes (suitable solutions for the problem)
#     [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
#         [New population] Create a new population by repeating following steps until the new population is complete
#         [Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
#         [Crossover] With a crossover probability cross over the parents to form a new offspring (children). If no crossover was performed, offspring is an exact copy of parents.
#         [Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
#         [Accepting] Place new offspring in a new population
#     [Replace] Use new generated population for a further run of algorithm
#     [Test] If the end condition is satisfied, stop, and return the best solution in current population
#     [Loop] Go to step 2

# ...existing imports...

class JSSP_Instance:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.n_jobs = 0
        self.n_machines = 0
        self.processing_times = None
        self.machine_sequence = None
        self.load_instance()

    def load_instance(self):
        """Load instance from text file"""
        try:
            with open(self.file_path, 'r') as f:
                # Skip empty lines and read until we find dimensions
                while True:
                    line = f.readline().strip()
                    if not line or line.startswith('#'):
                        continue
                    # Try to parse dimensions
                    try:
                        dimensions = [int(x) for x in line.split()]
                        if len(dimensions) >= 2:
                            self.n_jobs = dimensions[0]
                            self.n_machines = dimensions[1]
                            break
                    except ValueError:
                        continue

                # Initialize arrays
                self.processing_times = np.zeros((self.n_jobs, self.n_machines))
                self.machine_sequence = np.zeros((self.n_jobs, self.n_machines), dtype=int)
                
                # Read job data
                job_count = 0
                while job_count < self.n_jobs:
                    line = f.readline().strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    values = line.split()
                    if len(values) >= self.n_machines * 2:
                        for j in range(self.n_machines):
                            idx = j * 2  # Each pair has 2 numbers
                            self.machine_sequence[job_count][j] = int(values[idx])
                            self.processing_times[job_count][j] = float(values[idx + 1])
                        job_count += 1

                print(f"Successfully loaded instance with {self.n_jobs} jobs and {self.n_machines} machines")

        except FileNotFoundError:
            raise FileNotFoundError(f"Instance file not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading instance file: {str(e)}")

class JSSP_DEAP:
    def __init__(self, instance: JSSP_Instance):
        self.instance = instance
        self.n_jobs = instance.n_jobs
        self.n_machines = instance.n_machines
        self.toolbox = base.Toolbox()
        self.setup_toolbox()

    def evaluate_schedule(self, individual: List[int]) -> Tuple[float,]:
        """Calculate makespan for a job sequence using instance data"""
        # Initialize machine completion times and job progress
        machine_times = [0] * self.n_machines
        job_progress = [0] * self.n_jobs
        
        # For each operation in the sequence
        for job_id in individual:
            job = job_id - 1  # Convert to 0-based index
            current_step = job_progress[job]
            
            if current_step >= self.n_machines:
                continue
                
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
    # Get list of instance files
    current_dir = os.getcwd()

    # files = []
    # for file_path in os.listdir('.'):
    #     if os.path.isfile(os.path.join('.', file_path)):
    #         files.append(file_path)
    
    # Get the instances files
    instance_dir = os.path.join(current_dir, 'instancias')
    instance_files = [f for f in os.listdir(instance_dir) if f.endswith('.txt')]
    print(instance_files)

    results = []
    
    for instance_file in instance_files:
        print(f"\nProcessing instance: {instance_file}")
        
        # Load instance
        instance_path = os.path.join(instance_dir, instance_file)
        instance = JSSP_Instance(instance_path)

       
        # Initialize and run GA
        jssp = JSSP_DEAP(instance)
        pop, log, hof = jssp.run(
            pop_size=250,
            n_gen=500,
            cx_pb=0.65,
            mut_pb=0.05
        )

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

if __name__ == "__main__":
    main()
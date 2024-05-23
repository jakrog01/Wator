from AnalysisScripts.Strategies.RespectToStrategies.AbstractRespectToStrategy import AbstractRespectToStrategy
import matplotlib.pyplot as plt
from WaTorSimulation.SimualtionArea import SimulationArea
from multiprocessing import Pool
import numpy as np
from copy import deepcopy

class RespectToPredatorsInitStrategy(AbstractRespectToStrategy):
    def __init__(self, errorbars: bool, threads_count, count_to_average, iteration_per_step):
        self.__error_bars = errorbars
        self.__threads_count = threads_count
        self.__count_to_average = count_to_average
        self.__iteration_per_step = iteration_per_step

    def start_analysis(self, area_sizes_tuple, init_prey_populations_tuple, init_predators_populations_tuple, 
                        a_params_tuple, b_params_tuple, c_params_tuple, d_params_tuple):
            
            self.__init_predators_populations = list(init_predators_populations_tuple)
            self.__init_predators_populations.sort()
            self.__prepare_parameters_list(area_sizes_tuple, init_prey_populations_tuple, a_params_tuple, 
                                        b_params_tuple, c_params_tuple, d_params_tuple)
            
            for parameters in self.__parameters_list:
                self.__run_analysis(parameters)
    
    def __prepare_parameters_list(self, area_sizes_tuple, init_prey_populations_tuple, a_params_tuple,
                                  b_params_tuple, c_params_tuple, d_params_tuple):
        
        self.__parameters_list = []
        for area_size in area_sizes_tuple:
            for init_prey_population in init_prey_populations_tuple:
                for a_param in a_params_tuple:
                    for b_param in b_params_tuple:
                        for c_param in c_params_tuple:
                            for d_param in d_params_tuple:
                                self.__parameters_list.append([area_size, init_prey_population, a_param,
                                                                b_param, c_param, d_param])
                                
    def __run_analysis(self, params_list):
        pool_results = [[None for _ in range(self.__count_to_average)] for __ in range (len(self.__init_predators_populations))]
        
        if self.__threads_count > 0:
            pool = Pool(processes= self.__threads_count)
        else:
            pool = Pool()

        for predator_population_index, predator_population in enumerate(self.__init_predators_populations):
            if (predator_population + params_list[1]) > 100:
                print("PROBLEM WITH SIMULATION PARAMS")
                return
            for average_index in range(self.__count_to_average):
                area = SimulationArea(params_list[0], params_list[1], predator_population, params_list[2], params_list[3], params_list[4], 
                                      params_list[5])
                pool_results[predator_population_index][average_index] = pool.apply_async(self.perform_single_simulation, args=(deepcopy(area), ))
        pool.close()
        pool.join()

        output_values = [[result.get() for result in results] for results in pool_results]

        result = []
        result_std = []

        for values in output_values:
            result.append(np.mean(values))
            result_std.append(np.std(values))

        if self.__error_bars:
            self.__save_result_with_bars(result, result_std, params_list)
        else:
            self.__save_result_without_bars(result, params_list)
    
    def perform_single_simulation(self, area):
        for i in range(self.__iteration_per_step):
            area.step()
            if area.end_of_simulation():
                return (i+1)
        return (self.__iteration_per_step)
    
    def __save_result_with_bars(self, result, result_std, params_list):
        threshold = 0
        max = 0
        
        for index,b in enumerate(result):
            if b == self.__iteration_per_step:
                threshold =self.__init_predators_populations[index]
                break
            elif b > max:
                max = b
                threshold =self.__init_predators_populations[index]

        plt.errorbar(self.__init_predators_populations, result, yerr= result_std)
        plt.axvline(threshold, linestyle='-.', linewidth = 1, label = f"Threshold value = {round(threshold,2)}%", color = "grey")
        plt.xlabel("Initial predators population")
        plt.ylabel("Number of iterations")
        plt.savefig(f"AnalysisResults/png/IPredators{params_list[0]}_{params_list[1]}_{params_list[2]}_{params_list[3]}_{params_list[4]}_{params_list[5]}Graph{self.__iteration_per_step}_{self.__count_to_average}")
        plt.cla()

        with open(f"AnalysisResults/txt/IPredators{params_list[0]}_{params_list[1]}_{params_list[2]}_{params_list[3]}_{params_list[4]}_{params_list[5]}Results{self.__iteration_per_step}_{self.__count_to_average}.txt", 'w') as f:
            f.write(f"{result}")
            f.write("\n")
            f.write("\n")
            f.write(f"{result_std}")
    
    def __save_result_without_bars(self, result, params_list):
        threshold = 0
        max = 0
        
        for index,b in enumerate(result):
            if b == self.__iteration_per_step:
                threshold =self.__init_predators_populations[index]
                break
            elif b > max:
                max = b
                threshold =self.__init_predators_populations[index]

        plt.scatter(self.__init_predators_populations, result)
        plt.axvline(threshold, linestyle='-.', linewidth = 1, label = f"Threshold value = {round(threshold,2)}%", color = "grey")
        plt.xlabel("Initial predators population")
        plt.ylabel("Number of iterations")
        plt.savefig(f"AnalysisResults/png/IPredators{params_list[0]}_{params_list[1]}_{params_list[2]}_{params_list[3]}_{params_list[4]}_{params_list[5]}Graph{self.__iteration_per_step}_{self.__count_to_average}")
        plt.cla()

        with open(f"AnalysisResults/txt/IPredators{params_list[0]}_{params_list[1]}_{params_list[2]}_{params_list[3]}_{params_list[4]}_{params_list[5]}Results{self.__iteration_per_step}_{self.__count_to_average}.txt", 'w') as f:
            f.write(f"{result}")
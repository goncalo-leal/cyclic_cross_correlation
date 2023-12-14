'''
   Tomas Oliveira e Silva, November 2017
   Diogo Daniel Soares Ferreira, 76504
   Luis Davide Jesus Leira, 76514
  
   ACA 2017/2018


   Code Changed By Pedro Lopes

   Update to python3
'''

import math
import csv
import subprocess
import os
import argparse

def writeToCSV(text):
    with open('results.csv','w') as file:
        for line in text:
            file.write(line)

def do_executions(max_grid, max_block, max_power, executable):
    # Initial headers
    print(max_grid,'max_block', max_block, max_power, executable)
  
    data = "Grid X, Grid Y, Block X, Block Y, GPU Time, CPU Time, Initialization Time, Transfer from host to GPU, Transfer from GPU to host, Grid Dimensions, Block Dimensions\n"

    for i1 in range (0,int(math.ceil(math.log(max_grid,2)))):
        grid_x = 1 << i1
        for i2 in range (0,int(math.ceil(math.log(max_grid,2)))):
            grid_y = 1 << i2

            for i3 in range (0,int(math.ceil(math.log(max_block,2))+1)):
                block_x = 1 << i3
                for i4 in range (0,int(math.ceil(math.log(max_block,2))+1)):
                    block_y = 1 << i4
                    #print(i1,i2,i3,i4)
                    print(i1,i2,i3,i4,grid_x*grid_y*block_x*block_y)

                    
                    # Check if grid does not exceed the maximum size of GPU
                    # Compares with 1.0 because of float errors
                    if(block_x*block_y > max_block):
                        continue

                    
                    # If the grid and block match the matrix size,
                    # Calculate the GPU time
                    if(grid_x*grid_y*block_x*block_y==max_power):
                        print("D")
                        tempData = str(int(block_x))+", "+str(int(block_y))+", "+str(int(grid_x))+", "+str(int(grid_y))                    
                        execSc = [executable, '-a', str(int(block_x)),  '-s', str(int(block_y)),  '-d', str(int(grid_x)),  '-f', str(int(grid_y))]
                        print(execSc)
                        value = 0
                        done = False
                        # If the GPU is busy, try it again
                        while (not done):
                            proc = subprocess.Popen(execSc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            out, error = proc.communicate()
                          
                            if proc.returncode==0:
                                done = True
                                out = out.decode("utf-8")
                                print(f"\n\n{out.split(' ')}\n\n")
                                for idx, line in enumerate(out.split(' ')):
                                    print(line)
                                    # Get the times printed by the program
                                    if idx==28:
                                        init_time = float(line)
                                    if idx==43:
                                        copToGpu = float(line)
                                    if idx==50:
                                        gpu_value = float(line)
                                    elif idx==65:
                                        copToCpu = float(line)
                                    elif idx==70:
                                        cpu_value = float(line)
                                # Store the times on the right CSV format to be saved
                                if not( gpu_value and cpu_value and init_time and copToGpu and copToCpu):
                                    continue
                                tempData += ", "+str(gpu_value)+", "+str(cpu_value)+", "+str(init_time)+", "+str(copToGpu)+", "+str(copToCpu)
                                print(tempData)
                                data += tempData+"\n"
                            else:
                                print(error)
                                print("execError")
    writeToCSV(data)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='ProgramName',
                description='What the program does',
                epilog='Text at the bottom of help')
    parser.add_argument('-b', '--max-block', type=int,required=True,help="Maximum Threads per block", dest='max_block')
    parser.add_argument('-g', '--max-grid' , type=int, required=True,help="Maximum Threads per grid", dest='max_grid')
    parser.add_argument('-m', '--max-power', type=int,required=True,help="Maximum Threads", dest='max_power')
    parser.add_argument('-e', dest='executable',required=True,)
    args = parser.parse_args()
    do_executions(args.max_grid, args.max_block, args.max_power, args.executable)

import psutil
import os
import time
import torch
import torch.nn as nn
import random
import numpy as np
import math

from EETQ import quant_weights, preprocess_weights, w8_a16_gemm, quant_weights_gpu

def set_random_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)

if __name__ == '__main__':
    M = 1
    N = 13824
    K = 5120

    set_random_seed(1)
    input = torch.rand(M, K, dtype=torch.float16).cuda()
    # output = torch.zeros(M, N, dtype=torch.float16).cuda()
    torch_weights_cpu = torch.rand(K, N, dtype=torch.float16)
    print("torch_weights_cpu: ", torch_weights_cpu)
    output_tensor = torch.zeros(M, N, dtype=torch.float16).cuda()
    print(torch.max(torch_weights_cpu, axis=0))
    # test quant_weights
    # t1 = time.perf_counter()
    # for i in range(100):
    ref_torch_weights, processed_torch_weights, torch_weight_scales = quant_weights(torch_weights_cpu, torch.int8, True)
    # t2 = time.perf_counter()
    # print("time1 :", t2 - t1)
    print("ref_torch_weights: ", ref_torch_weights)
    print("processed_torch_weights: ", processed_torch_weights)
    print("torch_weight_scale: ", torch_weight_scales)
    # t1 = time.perf_counter()
    # for i in range(100):
    ref_torch_weights_gpu, processed_torch_weights_gpu, torch_weight_scales_gpu = quant_weights_gpu(torch_weights_cpu, torch.int8, True)
    
            
    # t2 = time.perf_counter()
    # print("time1 :", t2 - t1)
    print("ref_torch_weights_gpu: ", ref_torch_weights_gpu)
    print("processed_torch_weights_gpu: ", processed_torch_weights_gpu)
    print("torch_weight_scale_gpu: ", torch_weight_scales_gpu)
    print(torch.sum(processed_torch_weights_gpu - processed_torch_weights))
    for i in range(M):
        for j in range(K):
            if(ref_torch_weights_gpu[i, j] != ref_torch_weights[i, j]):
                print(i, j)
    for i in range(M):
        for j in range(K):
            if(processed_torch_weights_gpu[i, j] != processed_torch_weights[i, j]):
                print(i, j)
    # processed_torch_weights = processed_torch_weights.cuda()
    # torch_weight_scales = torch_weight_scales.cuda()
    # output = w8_a16_gemm(input, processed_torch_weights, torch_weight_scales)
    # print("out1: ", output)

    # # test preprocess_weights
    # processed_w = preprocess_weights(ref_torch_weights)
    # print("processed_w: ", processed_w)
    # processed_w = processed_w.cuda()
    # output = w8_a16_gemm(input, processed_w, torch_weight_scales)
    # print("out2: ", output)

    # # test torch matmul
    # ref_torch_weights = ref_torch_weights.to(torch.float16).cuda()
    # print("ref_torch_weights fp16: ", ref_torch_weights * torch_weight_scales)
    # torch_weights_cuda = torch_weights_cpu.cuda().to(torch.float16)
    # out_torch = torch.matmul(input, torch_weights_cuda)
    # print("out torch: ", out_torch)


    # torch.cuda.synchronize()
    # t1 = time.perf_counter()
    # for i in range(500):
    #     output = w8_a16_gemm(input, processed_torch_weights, torch_weight_scales)
    # torch.cuda.synchronize()
    # print(output)
    # print(torch.sum(output - out_torch))
    # t2 = time.perf_counter()
    # print("time: ", (t2 - t1) / 100)

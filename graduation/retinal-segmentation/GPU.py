import time
import torch

DURATION = 30
SIZE = 1024

if not torch.cuda.is_available():
    print("未检测到 CUDA GPU，无法进行显卡测试。")
    raise SystemExit(1)

device = torch.device("cuda")
print("GPU:", torch.cuda.get_device_name(0))
print(f"测试时间: {DURATION} 秒，矩阵大小: {SIZE}")
print("按 Ctrl+C 可随时停止。")

a = torch.randn((SIZE, SIZE), device=device)
b = torch.randn((SIZE, SIZE), device=device)

torch.cuda.synchronize()
start = time.time()
count = 0

try:
    while time.time() - start < DURATION:
        c = torch.mm(a, b)
        torch.cuda.synchronize()
        count += 1

        if count % 10 == 0:
            elapsed = time.time() - start
            print(f"已运行 {elapsed:.1f} 秒，完成 {count} 次计算")

except KeyboardInterrupt:
    print("\n已手动停止测试。")

finally:
    del a, b
    torch.cuda.empty_cache()
    print("测试结束。")
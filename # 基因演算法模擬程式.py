import pandas as pd
import random
import time

# ---- 使用者輸入工件數與時間 ----
num_jobs = int(input("請輸入工件數（例如10或14）："))

print("請輸入每個工件的 M1 加工時間（以空格分隔）：")
job_m1_times = list(map(int, input("M1 時間：").split()))
assert len(job_m1_times) == num_jobs, "輸入的 M1 數量與工件數不符"

print("請輸入每個工件的 M2 加工時間（以空格分隔）：")
job_m2_times = list(map(int, input("M2 時間：").split()))
assert len(job_m2_times) == num_jobs, "輸入的 M2 數量與工件數不符"

# ---- 固定參數 ----
max_generations = 50
patience = 10
M1_unavailable = (23, 26)
M2_unavailable = (28, 31)
max_batch_size = num_jobs

# ---- 定義函數 ----
def compute_m1_schedule(sequence):
    schedule = []
    current_time = 0
    for job in sequence:
        job_idx = int(job[1:]) - 1
        t = job_m1_times[job_idx]
        start = current_time
        end = start + t
        if start < M1_unavailable[1] and end > M1_unavailable[0]:
            start = M1_unavailable[1]
            end = start + t
        schedule.append((job, start, end))
        current_time = end
    return schedule

def compute_m2_batches(m1_schedule):
    batches = []
    temp = []
    for job in m1_schedule:
        temp.append(job)
        if len(temp) >= max_batch_size:
            batches.append(temp)
            temp = []
    if temp:
        batches.append(temp)

    print("--- M2 分批結果 ---")
    for i, batch in enumerate(batches):
        print(f"批次{i+1}: {[job[0] for job in batch]}")

    m1_end_times = {job: end for job, start, end in m1_schedule}
    m2_job_times = {f"J{i+1}": job_m2_times[i] for i in range(num_jobs)}

    current_start = 0
    batch_times = []
    for batch in batches:
        ready_time = max(m1_end_times[job] for job, _, _ in batch)
        process_time = max(m2_job_times[job] for job, _, _ in batch)
        start = max(current_start, ready_time)
        if start < M2_unavailable[1] and (start + process_time) > M2_unavailable[0]:
            start = M2_unavailable[1]
        end = start + process_time
        batch_times.append((batch, start, end))
        current_start = end

    return batch_times, batch_times[-1][2]

# ---- 開始計時 ----
start_time = time.time()

# ---- 初始設定 ----
jobs = [f"J{i+1}" for i in range(num_jobs)]
evolution_history = []

current_chrom = jobs.copy()
m1 = compute_m1_schedule(current_chrom)
m2, makespan = compute_m2_batches(m1)

best_makespan = makespan
best_solution = current_chrom.copy()
best_generation = 1
no_improve_count = 0

evolution_history.append({
    "世代": "第1代",
    "親代": current_chrom.copy(),
    "染色體": current_chrom.copy(),
    "交配動作": "無",
    "突變動作": "無",
    "總完成時間": makespan
})

# ---- 遺傳演化 ----
for gen in range(2, max_generations + 1):
    i_c, j_c = random.sample(range(len(current_chrom)), 2)
    after_cross = current_chrom.copy()
    job_i_c, job_j_c = after_cross[i_c], after_cross[j_c]
    after_cross[i_c], after_cross[j_c] = job_j_c, job_i_c

    m1_c = compute_m1_schedule(after_cross)
    m2_c, makespan_c = compute_m2_batches(m1_c)

    child_result = after_cross.copy()
    result_mutation = "無"
    final_makespan = makespan_c

    if abs(makespan_c - best_makespan) <= 2:
        i_m, j_m = random.sample(range(len(after_cross)), 2)
        after_mut = after_cross.copy()
        job_i_m, job_j_m = after_mut[i_m], after_mut[j_m]
        after_mut[i_m], after_mut[j_m] = job_j_m, job_i_m
        m1_m = compute_m1_schedule(after_mut)
        m2_m, makespan_m = compute_m2_batches(m1_m)
        child_result = after_mut.copy()
        result_mutation = f"{job_i_m} ↔ {job_j_m}"
        final_makespan = makespan_m
        current_chrom = after_mut
    else:
        current_chrom = after_cross

    if final_makespan < best_makespan:
        best_makespan = final_makespan
        best_solution = child_result.copy()
        best_generation = gen
        no_improve_count = 0
    else:
        no_improve_count += 1

    evolution_history.append({
        "世代": f"第{gen}代",
        "親代": evolution_history[-1]["染色體"].copy(),
        "染色體": child_result.copy(),
        "交配動作": f"{job_i_c} ↔ {job_j_c}",
        "突變動作": result_mutation,
        "總完成時間": final_makespan
    })

    if no_improve_count >= patience and gen >= 50:
        evolution_history.append({
            "世代": f"🔴 注意：第{gen}代起連續10代無改善",
            "親代": "",
            "染色體": "",
            "交配動作": "",
            "突變動作": "",
            "總完成時間": ""
        })
        break

# ---- 結果輸出 ----
for row in evolution_history:
    print(row)

print("✅ 完成模擬")
print(f"🔎 最佳解出現在第 {best_generation} 代，完工時間為 {best_makespan} 分鐘")
print("最佳染色體排序：", best_solution)

end_time = time.time()
total_time = end_time - start_time
print(f"⏱️ 總模擬時間：約 {total_time:.2f} 秒") 



if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
import subprocess
import os
import sys
import time

@custom
def run_dbt(*args, **kwargs):
    # 1. Use the ABSOLUTE path. 
    dbt_base_path = "/home/src/news_report"
    absolute_db_path = "/home/src/data/news_report.duckdb" 
    #In docker compose i mapped ./data to home/src/data
    print("⏳Waiting for DuckDB file locks to clear ...")
    time.sleep(2)
 
    # 2. Tell dbt EXACTLY where to find the profiles.yml
    # We use the absolute path so there is no guessing.
    os.environ['DBT_PROFILES_DIR'] = dbt_base_path
    os.environ['DB_PATH'] = absolute_db_path

    # 3. Construct the command using the absolute path
    # 'dbt build' is the Pro move—it runs seeds, models, and tests in order.
    db_dir = os.path.dirname(absolute_db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, 
                    exist_ok)
        print(f"📁 Created missing directory: {db_dir}")

    cmd = f"cd {dbt_base_path} &&\
            dbt build"
    
    print(f"🚀 Launching dbt from: {absolute_db_path}")
    print(f"Executing: {cmd}")

    # 4. Execute
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    output_log = []
    for line in process.stdout: # Stream output realtime in console
        sys.stdout.write(line)
        sys.stdout.flush()
        output_log.append(line)

    process.wait()
    
    # 5. Professional Logging
    if process.returncode == 0:
        print("✅ DBT SUCCESS")
        # Optional: print(process.stdout) if you want to see the table names in Mage logs
        return "Pipeline Orchestration Complete"
    else:
        print("\n❌ DBT FAILED \n\t\t {process.returncode}")
        # We print both stdout and stderr because dbt often puts errors in stdout
        error_msg = "".join(output_log)
        raise Exception(f"dbt failed. Final logs:\n{error_msg}.")
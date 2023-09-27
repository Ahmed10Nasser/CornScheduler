from CronScheduler import CronScheduler


def hello(name : str = "Ahmed", sleepTime : int = 5):
  import time
  time.sleep(sleepTime)
  print("Hello "+name+"!")


cron_scheduler = CronScheduler()

"""
  The following job1 runs evety minute, 
  and the given expected runtime is 90s, 
  and the acutal is 90s, 
  so there will be concurrent instances of the same job,
  and it's handled because of the given expected runtime >= the actual runtime
"""
cron_scheduler.schedule_job(id="job1", expected_runtime_in_seconds=90, cron_expression="* * * * *", job_function=hello, job_function_args=["Ahmed", 90])

"""
  The following job2 runs evety two minutes, 
  and the expected runtime is 30s, 
  and the acutal is 15s,
  and there are no concurrent instances
"""
cron_scheduler.schedule_job(id="job2", expected_runtime_in_seconds=30, cron_expression="*/2 * * * *", job_function=hello, job_function_args=["Nasser", 15])

"""
  The following job3 runs evety minute, 
  and the given expected runtime is 30s, 
  but the acutal is 90s, 
  so there will be concurrent instances of the same job,
  but the given expected runtime is < the actual runtime,
  so some concurrent instances may be skipped
"""

cron_scheduler.schedule_job(id="job3", expected_runtime_in_seconds=30, cron_expression="* * * * *", job_function=hello, job_function_args=["Zaki", 90])

cron_scheduler.start_scheduler()

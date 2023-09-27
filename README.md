# CronScheduler
## Brief description of the solution
- I have implemented a class named `CronScheduler` using `apscheduler` package.
- The main method for the class is `schedule_job` that takes these following parameters and returns `bool` indicating whether the job has been scheduled or not.
```python
def schedule_job(self,
                  *,
                 id : str,
                 expected_runtime_in_seconds : int,
                 cron_expression : str,
                 job_function : any,
                 job_function_args : list) -> bool :
```
- The  `schedule_job` method works as following :
    - Doing some validations for the job `id` uniqueness and `cron_expression` validation.
    - Calculating the max needed number of job instances that can run **concurrently**. This is calculated depending on the given `expected_runtime_in_seconds` interval and the `cron_expression` frequency.
    - Addin the job to the scheduler with all pre-calculated needed parameters.
- I have added some listeners to the cron scheduler to log :
    - when a job instance begins to execute.
    - when a job instance finishs execution and how much time it takes.
- I have wrote some tests for the the job validations (id uniqueness and cron validation).
- I have used docker, so anyone can easily run it.

## Reasoning behind the technical decisions
In the phase of searching, I came cross two packages that I can use to schedule cron jobs which are `apscheduler` and `python-crontab`.
I have decide to go with `apscheduler` beacuse:
- `python-crontab` is just a simple tool that can write,read and manipulate your system crontab file.
- `apscheduler` package is more controlling over the cron jobs and you can use its functions and listeners to make some instruments and calculations for the jobs

## Examples to schedule a cron job
The following function is the job that will be scheduled many times with different parametrs :
```python
def hello(name : str = "Ahmed", sleepTime : int = 5):
  import time
  time.sleep(sleepTime)
  print("Hello "+name+"!")
```
The following `job1` runs **evety minute**, and the given expected runtime is **90s**, and the acutal runtime is **90s**, so there will be **concurrent instances** of the same job, and it's handled because of the given expected runtime **>=** the actual runtime:
```python
cron_scheduler.schedule_job(id="job1",
                            expected_runtime_in_seconds=90,
                            cron_expression="* * * * *",
                            job_function=hello,
                            job_function_args=["Ahmed", 90])
```
The following `job2` runs **evety two minutes**, and the expected runtime is 30s, 
and the acutal is **15s**, and there are **no concurrent instances** .
```python
cron_scheduler.schedule_job(id="job2",
                            expected_runtime_in_seconds=30,
                            cron_expression="*/2 * * * *",
                            job_function=hello,
                            job_function_args=["Nasser", 15])
```
The following `job3` runs **evety minute**, and the given expected runtime is **30s**, but the acutal is **90s**, so there will be **concurrent instances** of the same job, but the given expected runtime is **<** the actual runtime, so some concurrent instances may be **skipped**.
```python
cron_scheduler.schedule_job(id="job3",
                            expected_runtime_in_seconds=30,
                            cron_expression="* * * * *",
                            job_function=hello,
                            job_function_args=["Zaki", 90])
```

## Possible future improvements
- 	Making the scheduler persistent by storing the jobs into some database.

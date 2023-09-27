class CornScheduler:
  
  from apscheduler.schedulers.background import BlockingScheduler
  from apscheduler import events
  import datetime
  from cron_validator import CronValidator
  
  def __init__(self):
    self.__scheduler = self.BlockingScheduler()
  

  def __job_started_listener(self, event):
    print("Starting a new instance of the job with id ({})".format(event.job_id))

  def __job_finished_listener(self, event):
    time_taken = self.datetime.datetime.now() - event.scheduled_run_time.replace(tzinfo=None)
    print("Finishing an instance of the job with id ({}) with taken time equals to {}".format(event.job_id, time_taken))

  def schedule_job(self,
                  *,
                 id : str,
                 expected_runtime_in_seconds : int,
                 cron_expression : str,
                 job_function : any,
                 job_function_args : list) -> bool :
  
    # Check for id uniqueness
    if self.__scheduler.get_job(id) is not None:
      return False

    # Check if the cron expression if valid
    try:
      self.CronValidator.parse(cron_expression)
    except:
      return False


    # Count the max needed number of job instrances that can run concurrently
    time_now = self.datetime.datetime.now()
    time_after_one_run = time_now + self.datetime.timedelta(seconds=expected_runtime_in_seconds)
    max_instances = max(1, len([ time for time in self.CronValidator.get_execution_time(expression=cron_expression, from_dt=time_now, to_dt=time_after_one_run)]))

    cron_list = cron_expression.split(" ")
    
    self.__scheduler.add_job(id=id,
                      func=job_function,
                      args=job_function_args,
                      max_instances= max_instances,
                      coalesce = True,
                      trigger="cron",
                      minute=cron_list[0],
                      hour=cron_list[1],
                      day=cron_list[2],
                      month=cron_list[3],
                      day_of_week=cron_list[4])

    return True
  
  def start_scheduler(self):
    self.__scheduler.add_listener(self.__job_started_listener, self.events.EVENT_JOB_SUBMITTED)
    self.__scheduler.add_listener(self.__job_finished_listener, self.events.EVENT_JOB_EXECUTED)
    self.__scheduler.start()
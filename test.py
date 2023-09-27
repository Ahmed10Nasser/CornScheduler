import unittest
from CronScheduler import CornScheduler

class TestDeclinedJobs(unittest.TestCase):
  
  def test_declined_job_for_id_uniqueness(self):
    cron_scheduler = CornScheduler()
    cron_scheduler.schedule_job(id="s1", expected_runtime_in_seconds=90, cron_expression="* * * * *", job_function=lambda name : print(name), job_function_args=["Nasser"])
    ret = cron_scheduler.schedule_job(id="s1", expected_runtime_in_seconds=90, cron_expression="* * * * *", job_function=lambda name : print(name), job_function_args=["Nasser"])
    self.assertFalse(ret)

  def test_declined_job_for_cron_validation(self):
    cron_scheduler = CornScheduler()
    ret = cron_scheduler.schedule_job(id="s1", expected_runtime_in_seconds=90, cron_expression="A * * * *", job_function=lambda name : print(name), job_function_args=["Nasser"])
    self.assertFalse(ret)

if __name__ == '__main__':
    unittest.main()
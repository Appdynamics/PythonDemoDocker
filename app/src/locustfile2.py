from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task
    def showSignUp(self):
        self.client.get("/signUp")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=1000
    max_wait=2000

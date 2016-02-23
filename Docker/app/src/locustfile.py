from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    @task
    def home(self):
        self.client.get("/")

    @task
    def showSignUp(self):
        self.client.get("/showSignUp")

    @task
    def http(self):
        self.client.get("/http")

    @task
    def viewCatalog(self):
        self.client.get("/viewCatalog")

    @task
    def addToCart(self):
        self.client.get("/addToCart")

    @task
    def checkout(self):
        self.client.get("/checkout")

    @task
    def viewCart(self):
        self.client.get("/viewCart")

    @task
    def viewCartRemoveItem(self):
        self.client.get("/viewCart-removeItem")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=10000
    max_wait=20000

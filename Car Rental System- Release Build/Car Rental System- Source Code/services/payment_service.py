class PaymentService:
    def __init__(self, repo): self.repo=repo
    def record(self,*args): self.repo.create(*args)

class CarService:
    def __init__(self, repo): self.repo=repo
    def add(self, car): self.repo.add(car)
    def update(self, car): self.repo.update(car)
    def delete(self, car_id): self.repo.delete(car_id)
    def all(self): return self.repo.all()
    def available(self): return self.repo.available()

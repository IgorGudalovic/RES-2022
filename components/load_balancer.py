class LoadBalancer:
    buffer = []

    # Prima podatke od Writer komponente
    def ReceiveData(self, data):
        pass

    # Prosledjuje primljene podatke slobodnim Workerima
    # Salje podatke koristeci Description strukturu
    def ForwardData(self):
        pass

from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "Nissan", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    # Use get_or_create to prevent duplicates
    car_make_instances = {
        data["name"]: CarMake.objects.get_or_create(**data)[0]
        for data in car_make_data
    }

    car_model_data = [
        {"name": "Pf", "type": "SUV", "year": 2023, "car_make": "Nissan"},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": "Nissan"},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": "Nissan"},
        {"name": "A-C", "type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "C-C", "type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "E-C", "type": "SUV", "year": 2023, "car_make": "Mercedes"},
        {"name": "A4", "type": "SUV", "year": 2023, "car_make": "Audi"},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": "Audi"},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": "Audi"},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": "Kia"},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": "Kia"},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": "Kia"},
        {"name": "Coro", "type": "Sedan", "year": 2023, "car_make": "Toyota"},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": "Toyota"},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": "Toyota"},
    ]

    # Create CarModel instances efficiently using bulk_create
    car_models = [
        CarModel(
            name=data["name"],
            car_make=car_make_instances[data["car_make"]],
            type=data["type"],
            year=data["year"],
        )
        for data in car_model_data
    ]
    CarModel.objects.bulk_create(car_models, ignore_conflicts=True)

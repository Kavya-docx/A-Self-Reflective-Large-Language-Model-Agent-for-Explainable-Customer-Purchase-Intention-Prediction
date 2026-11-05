import argparse

from purchase_intention.data import generate_dataset
from purchase_intention.model import PurchaseModel

parser = argparse.ArgumentParser(description="Train the local purchase intention model")
parser.add_argument("--samples", type=int, default=4000)
parser.add_argument("--seed", type=int, default=42)
args = parser.parse_args()
bundle = generate_dataset(args.samples, args.seed)
model = PurchaseModel.train(bundle, args.seed)
model.save("models/purchase_model.joblib")
print(model.metrics)
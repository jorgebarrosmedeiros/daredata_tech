import pickle
import pandas as pd

model = pickle.load(open("models/model.sav", "rb"))


def predict(values):

    for value in values:
        df = pd.DataFrame.from_dict(value, orient="index").T

        df.columns = ["attr_a", "attr_b", "scd_a", "scd_b"]
        #
        label_encoder = {"a": 0, "b": 1, "c": 2, "d": 3}
        df["attr_b"] = df["attr_b"].map(label_encoder)

        response = model.predict(df)[0]
        value["response"] = response

    return str(value)

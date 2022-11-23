from typing import Iterable, Any
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import pickle
import xgboost
from imblearn import combine as c
from logger import logger
from os.path import expanduser


class MLEModel:
    def load(self, *args, **kwargs) -> Any:
        """
        Loads the model and any required artifacts.
        To be implemented by the data scientist.
        """
        logger.info("Initialize Load Machine Learning Model")

        try:
            model = pickle.load(
                open(
                    "./modules/ds/models/model.sav",
                    "rb",
                )
            )
            return model
        except Exception as err:
            error_message = f"*Error trying to load model!*\n {err}"
            logger.exception(error_message)
            raise Exception

    def load_database(self, *args, **kwargs) -> None:
        """
        Saves the model and any required artifacts to a given location.
        To be implemented by the data scientist.
        """
        logger.info("Initialize Load Feature Store")

        try:
            # Create an engine instance
            alchemyEngine = create_engine(
                "postgresql+psycopg2://ds_user:ds_user@localhost/companydata"
            )

            # Connect to PostgreSQL server
            dbConnection = alchemyEngine.connect()
            # Read data from PostgreSQL database table and load into a DataFrame instance
            query = """
					select fs2.* from feature_store fs2 
			"""
            dataFrame = pd.read_sql(query, dbConnection)
            return dataFrame

        except Exception as err:
            error_message = f"*Error trying to load model!*\n {err}"
            logger.exception(error_message)
            raise Exception

    def save(self, model) -> None:
        """
        Saves the model and any required artifacts to a given location.
        To be implemented by the data scientist.
        """
        logger.info("Initialize Save Machine Learning Model")
        try:
            filename = "models/model.sav"
            pickle.dump(model, open(filename, "wb"))
            return logger.info("Model Save: Success")
        except Exception as err:
            error_message = f"*Error trying to save model!*\n {err}"
            logger.exception(error_message)
            raise Exception

    def fit(self, data, model):
        """Fits the model to the data. To be implemented by the data scientist."""
        logger.info("Initialize fit Machine Learning Model")
        try:

            # define sampler
            smt = c.SMOTETomek(sampling_strategy="auto", random_state=32, n_jobs=-1)

            # apply sampler
            x_smt, y_smt = smt.fit_resample(data, data["label"])

            # model definition
            xgb_model = model.XGBClassifier(n_jobs=-1)

            # fit model
            xgb_model.fit(x_smt, y_smt)
            return logger.info("Model Fitted: Success")

        except Exception as err:
            error_message = f"*Error fit model!*\n {err}"
            logger.exception(error_message)
            raise Exception

    def predict(self, features, model) -> int:
        """Predicts the label of unseen data. To be implemented by the data scientist."""
        logger.info("Predicting Results")
        try:
            df = pd.DataFrame.from_dict(features, orient="index").T
            df.columns = ["attr_a", "attr_b", "scd_a", "scd_b"]
            label_encoder = {"a": 0, "b": 1, "c": 2, "d": 3}
            df["attr_b"] = df["attr_b"].map(label_encoder)
            response = model.predict(df)[0]
            features["response"] = response
            return features
        except Exception as err:
            error_message = f"*Error predict values!*\n {err}"
            logger.exception(error_message)
            raise Exception

        raise NotImplementedError()

    def predict_with_logging(self, client_idx: int, features: Any) -> None:
        """
        Calls the predict function, implemented by the data scientist, and logs the results
        of the prediction to storage.
        """
        predicted_label = self.predict(features)
        self.log_to_storage(client_idx, predicted_label)

        return predicted_label

    def log_to_storage(self, client_idx: int, predicted_label: int):
        """
        Logs the prediction to the predictions table, on the database.
        Our extremely advanced "storage" is a text file on the `~/mle_storage` directory :-)
        """
        try:
            with open(f'{expanduser("~")}/mle_storage/labels', "a+") as f:
                f.write(f"{client_idx},{predicted_label}\n")
        except FileNotFoundError:
            print("Have you created the ~/mle_storage directory?")

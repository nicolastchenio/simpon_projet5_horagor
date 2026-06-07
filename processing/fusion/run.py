# processing/fusion/run.py

from processing.fusion.merger import FusionEngine


class FusionPipeline:

    def __init__(self):
        self.engine = FusionEngine()

    def run(self, matches, tmdb_data, kaggle_data=None, imdb_data=None, rotten_data=None):

        return self.engine.merge(
            matches, 
            tmdb_data, 
            kaggle_data=kaggle_data, 
            imdb_data=imdb_data, 
            rotten_data=rotten_data
        )
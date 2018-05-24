from markov import MarkovModel
import pickle
import argparse
import os


def console():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Path to the binary with the model")
    parser.add_argument("--seed", help="Seed word for the model")
    parser.add_argument("--length", help="Length of the generated sequence", type=int)
    parser.add_argument("--output", help="Path to file to save sequence")
    args_parsed = parser.parse_args()
    return args_parsed


class SentenceGenerator():
    def __init__(self, model, length, seed, output):
        self.model_dist = model
        self.length = length
        self.seed = seed
        self.output = output
        self.model = None

    def load_model(self):
        model_file = None
        try:
            model_file = open(self.model_dist, "rb")
        except:
            raise RuntimeError("Please, sprecify file with model correctly")
        model = None
        try:
            model = pickle.load(model_file)
        except:
            raise RuntimeError("Problems loading the model from the file")
        self.model = model

    def gen_sent(self):
        if self.model is None:
            raise RuntimeError("Model was not loaded")
        if type(self.length) is not int or self.length < 0:
            raise RuntimeError("Length of the random sequence is not specified or is incorrect")

        if self.seed is not None and (self.seed,) not in set(self.model):
            print("Your seed is not valid or specified. Choosing random")
            self.seed = None
        self.sentence = self.model.random_sent(length=self.length, seed_word=self.seed)

    def save_sentence(self):
        if self.output is None:
            print(self.sentence)
            return
        _, extension = os.path.splitext(self.output)

        if extension != ".txt":
            raise RuntimeWarning("The recommended dist is  a .txt file")
        dist = None
        try:
            dist = open(self.output, "w+")
        except:
            print("Destination doesn't exist. Creating file")
            dir = os.path.dirname(self.output)
            if not os.path.exists(dir):
                print("Directory does not exist. Creating directory")
                os.mkdir(dir)
            os.mknod(self.output)
            dist = open(self.output, "w+")
        dist.write(self.sentence)


def main():
    args = console()
    generator = SentenceGenerator(length=args.length, model=args.model,
                                  seed=args.seed, output=args.output)
    generator.load_model()
    generator.gen_sent()
    generator.save_sentence()


if __name__ == "__main__":
    main()

from english_words import get_english_words_set
import click
import matplotlib.pyplot as plt
from itertools import product
from utils import timer


class Sorcerer:

    def __init__(self, debug, mode):
        self.word = None
        self.debug = debug
        self.mode = mode
        self.keyboard = self.get_keyboard()
        self.corpus = self.prepare_corpus()
        if self.debug:
            self.describe_corpus()

    def generate_corpus(self, count):
        corpus = {}
        for i in range(count):
            corpus[i + 1] = []

        return corpus

    def prepare_corpus(self):
        words = get_english_words_set(['web2'], lower=True)
        if self.debug:
            print('There are ' + str(len(words)) + ' words')
        corpus = self.generate_corpus(28)
        longest = 0
        for word in words:
            count = len(word)
            corpus[count].append(word)
            if count > longest:
                longest = count
                longest_word = word

        if self.debug:
            print('The longest word is ' + longest_word)
            print('It\'s lenght is ' + str(longest))

        return corpus

    def describe_corpus(self):
        counts = [len(list) for i, list in self.corpus.items()]
        container = plt.bar(range(1, len(counts) + 1), counts)
        plt.bar_label(container, counts, label_type='edge')
        plt.axis('on')
        plt.show()

    def get_keyboard(self):
        return {
            0: ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            1: ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            2: ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        }

    def find_element_in_keyboard(self, element):
        for key, value_list in self.keyboard.items():
            if element in value_list:
                return key, value_list.index(element)
        return None, None

    def word_to_keyboard(self, word):
        return [self.find_element_in_keyboard(letter) for letter in word]

    def keyboard_to_letter(self, letter):
        row, column = letter
        return self.keyboard.get(row)[column]

    def keyboard_to_word(self, word):
        return ''.join([self.keyboard_to_letter(letter) for letter in word])

    def get_permutations(self, position):
        row, column = position
        possible_rows = [row - 1, row, row + 1]
        possible_columns = [column - 1, column, column + 1]

        # removing impossible values
        possible_rows = [item for item in possible_rows if 0 <= item <= 2]
        possible_columns = [item for item in possible_columns if 0 <= item <= 9]
        possible_permutations = list(product(possible_rows, possible_columns))

        if possible_columns[len(possible_columns) - 1] >= 6:
            possible_permutations = [p for p in possible_permutations if self.validate_permutation(p) is not None]

        return possible_permutations

    def generate_misspells(self):
        positions = self.word_to_keyboard(self.word)
        permutations = []
        for position in positions:
            permutations.append(self.get_permutations(position))

        all_combinations = []

        for i in range(len(positions)):
            for variation in permutations[i]:
                # Create a new list with the ith element replaced by its variation
                new_combination = positions[:i] + [variation] + positions[i + 1:]
                all_combinations.append(new_combination)

        return all_combinations

    def generate_swaps(self):
        all_combinations = []

        positions = self.word_to_keyboard(self.word)

        for i in range(len(positions) - 1):
            # Swap adjacent elements
            positions[i], positions[i + 1] = positions[i + 1], positions[i]
            all_combinations.append(positions.copy())
            # Swap back to restore original list
            positions[i], positions[i + 1] = positions[i + 1], positions[i]

        return all_combinations

    def generate_variants(self):
        misspells = self.generate_misspells()
        swaps = self.generate_swaps()

        variants = misspells + swaps

        # Use a set to keep track of unique lists (converted to tuples of tuples)
        seen = set()

        # Store the unique lists here
        unique_lists = []

        for lst in variants:
            # Convert the list of tuples to a tuple of tuples
            tuple_version = tuple(lst)

            # If this tuple of tuples is not in the set, it's unique
            if tuple_version not in seen:
                seen.add(tuple_version)
                unique_lists.append(lst)

        return unique_lists

    def predict(self, word):
        self.word = word
        variants = self.generate_variants()
        suggestions = []
        for variant in variants:
            suggestions.append((self.keyboard_to_word(variant), self.get_suggestions(len(word), variant)))

        if self.debug:
            for variant, suggestion_list in suggestions:
                print("The word you typed is: {}".format(word))
                print("Calculating suggestions for variant: {}".format(variant))
                print("The best 10 suggestions are: ")
                for suggestion, distance in suggestion_list:
                    print("The word {}, with a total distance of {}".format(suggestion, distance))

        results = self.results(suggestions)

        if self.mode == 'slim':
            variant, (word, distance) = results[0]
            return word
        else:
            self.display_results(results)

    def validate_permutation(self, permutation):
        row, column = permutation
        try:
            return self.keyboard.get(row)[column]
        except IndexError:
            return None

    def get_suggestions(self, count, variant):
        corpus = self.corpus[count]
        distances = []
        for word in corpus:
            distances.append(sum(self.calculate_distance(word, variant)))

        sorted_with_index = sorted(enumerate(distances), key=lambda x: x[1])

        return [(corpus[index], element) for index, element in sorted_with_index[:5]]

    def calculate_distance(self, word, variant):
        encoded_word = self.word_to_keyboard(word)
        return [sum((abs(a - c), abs(b - d))) for (a, b), (c, d) in zip(encoded_word, variant)]

    def results(self, suggestions):
        # Flatten the structure
        flattened_data = [(word, variant, distance) for word, data in suggestions for variant, distance in data]

        # Dictionary to store the minimum distance for each variant
        min_distances = {}

        for word, variant, distance in flattened_data:
            if variant not in min_distances or distance < min_distances[variant][1]:
                min_distances[variant] = (word, distance)

        return sorted(min_distances.items(), key=lambda x: x[1][1])

    def display_results(self, results):
        for variant, (word, distance) in results[:10]:
            print(f"From the input: {word}, our guess is: {variant}, Distance: {distance}")


@click.command()
@click.option("--word", "-w", prompt="What is your word ? ")
# @click.option("--word", "-w", default='tesla')
@click.option("--debug", "-d", default=False)
@click.option("--mode", "-m", default="slim")
@timer
def main(word, debug, mode):
    sorcerer = Sorcerer(debug, mode)
    predicted = sorcerer.predict(word)
    print(predicted)


if __name__ == '__main__':
    main()

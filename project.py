from itertools import product, chain

import click
import matplotlib.pyplot as plt
import re
from english_words import get_english_words_set

from utils import timer
from multiprocessing import Pool


class Sorcerer:

    def __init__(self, debug, mode):
        self.word = None
        self.debug = debug
        self.mode = mode
        self.keyboard = self.get_keyboard()
        self.reverse_keyboard = {v: k for k, v in self.keyboard.items()}
        self.corpus = self.prepare_corpus()
        if self.debug:
            self.describe_corpus()

    def generate_corpus(self, count):
        return {i: [] for i in range(1, count + 1)}

    def contains_chars(self, string, char_set):
        pattern = f"[{''.join(char_set)}]"
        return bool(re.search(pattern, string))


    def prepare_corpus(self):
        words = get_english_words_set(['web2'], lower=True)
        if self.debug:
            print('There are ' + str(len(words)) + ' words')
        corpus = self.generate_corpus(28)
        longest = 0
        for word in words:
            count = len(word)
            if not self.contains_chars(word, {'-'}):
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
        keyboard_layout = {
            'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4),
            'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
            'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4),
            'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8),
            'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4),
            'n': (2, 5), 'm': (2, 6)
        }
        return keyboard_layout

    def find_element_in_keyboard(self, element):
        return self.keyboard.get(element, (None, None))

    def word_to_keyboard(self, word):
        return [self.find_element_in_keyboard(letter) for letter in word]

    def keyboard_to_letter(self, keyboard):
        return self.reverse_keyboard.get(keyboard, None)

    def keyboard_to_word(self, word):
        return ''.join([self.keyboard_to_letter(letter) for letter in word])

    def get_permutations(self, position):
        row, column = position
        possible_rows = [r for r in [row - 1, row, row + 1] if 0 <= r <= 2]
        possible_columns = [c for c in [column - 1, column, column + 1] if 0 <= c <= 9]
        possible_permutations = list(product(possible_rows, possible_columns))
        if column >= 6:
            possible_permutations = [p for p in possible_permutations if self.validate_permutation(p)]

        return possible_permutations

    def generate_misspells_parallel(self, args):
        index, permutations, positions = args
        return [positions[:index] + [variation] + positions[index + 1:] for variation in permutations]

    def generate_misspells(self):
        with Pool() as pool:
            positions = self.word_to_keyboard(self.word)
            permutations = pool.map(self.get_permutations, positions)
            #preparing parallelization...
            args = [(i, permutations[i], positions) for i in range(len(positions))]
            all_combinations = pool.map(self.generate_misspells_parallel, args)
            return list(chain.from_iterable(all_combinations))

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
        seen = set()
        # Removing duplicates using a list comprehension and a set
        return [lst for lst in variants if not (t := tuple(lst)) in seen and not seen.add(t)]


    def predict(self, word):
        self.word = word
        variants = self.generate_variants()
        with Pool() as pool:
            suggestions = pool.starmap(self.get_suggestions,
                                       [(len(word), variant) for variant in variants])

        if self.debug:
            self.display_debug_info(suggestions)

        results = self.results(suggestions)

        if results and self.mode == 'slim':
            variant, (word, distance) = results[0]
            return word
        else:
            self.display_results(results)

    def display_debug_info(self, suggestions):
        for variant, suggestion_list in suggestions:
            print("The word you typed is: {}".format(self.word))
            print("Calculating suggestions for variant: {}".format(variant))
            print("The best 10 suggestions are: ")
            for suggestion, distance in suggestion_list:
                print("The word {}, with a total distance of {}".format(suggestion, distance))

    def validate_permutation(self, permutation):
        try:
            return self.keyboard_to_letter(permutation)
        except IndexError:
            return None

    def get_suggestions(self, word_length, variant):
        distances = [sum(self.calculate_distance(word, variant)) for word in self.corpus[word_length]]
        sorted_with_index = sorted(enumerate(distances), key=lambda x: x[1])
        return [(self.keyboard_to_word(variant), self.corpus[word_length][index], element) for index, element in sorted_with_index[:5]]


    def calculate_distance(self, word, variant):
        encoded_word = self.word_to_keyboard(word)
        # print(self.keyboard_to_word(variant))
        # updated_list = [(0, 0) if x == (None, None) else x for x in encoded_word]
        # print(self.keyboard_to_word(updated_list))
        return [sum((abs(a - c), abs(b - d))) for (a, b), (c, d) in zip(encoded_word, variant)]

    def results(self, suggestions):
        min_distances = {}
        for word, variant, distance in list(chain.from_iterable(suggestions)):
            if variant not in min_distances or distance < min_distances[variant][1]:
                min_distances[variant] = (word, distance)

        return sorted(min_distances.items(), key=lambda x: x[1][1])

    def display_results(self, results):
        for variant, (word, distance) in results[:10]:
            print(f"From the input: {word}, our guess is: {variant}, Distance: {distance}")


@click.command()
@click.option("--word", "-w", default='information', help="The word to predict variants for.")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode.")
@click.option("--mode", "-m", default="slim", type=click.Choice(['slim', 'full']), help="Output mode: 'slim' or 'full'.")
@timer
def main(word, debug, mode):
    sorcerer = Sorcerer(debug, mode)
    predicted = sorcerer.predict(word)
    if mode == 'slim':
        print(predicted)


if __name__ == '__main__':
    main()

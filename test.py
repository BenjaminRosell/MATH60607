from project import Sorcerer
from utils import timer

@timer
def main():
    test_cases = [
        ('newspaler', 'newspaper'),
        ('informagion', 'information'),
        ('backrround', 'background'),
        ('oppodtunity', 'opportunity'),
        ('importnat', 'important'),
        ('marleting', 'marketing'),
        ('protecgion', 'protection'),
        ('produdtion', 'production'),
        ('develolment', 'development'),
        ('environnent', 'environment'),
        ('umiversity', 'university'),
        ('popukation', 'population'),
        ('ddpartment', 'department'),
        ('apqrtment', 'apartment'),
        ('comnitment', 'commitment'),
        ('responsivle', 'responsible'),
        ('discuwsion', 'discussion'),
        ('spectqcular', 'spectacular'),
        ('chocplate', 'chocolate'),
        ('partifular', 'particular'),
        ('tradigional', 'traditional'),
        ('diffisulty', 'difficulty'),
        ('cimmercial', 'commercial'),
        ('ewucation', 'education'),
        ('sometying', 'something'),
        ('operayion', 'operation'),
        ('journqlist', 'journalist'),
        ('celebrayion', 'celebration'),
        ('manafement', 'management'),
        ('edpecially', 'especially'),
        ('experirnce', 'experience'),
        ('relatjonship', 'relationship'),
        ('conferfnce', 'conference'),
        ('associstion', 'association'),
        ('ligerature', 'literature'),
        ('prdsident', 'president'),
        ('tecjnology', 'technology'),
        ('colkection', 'collection'),
        ('induatrial', 'industrial'),
        ('difrerence', 'difference'),
        ('voluntwer', 'volunteer'),
        ('conmunity', 'community'),
        ('remaruable', 'remarkable'),
        ('investmejt', 'investment'),
        ('succesqful', 'successful'),
        ('sugrestion', 'suggestion'),
        ('thriughout', 'throughout'),
        ('achiebement', 'achievement'),
        ('sectetary', 'secretary'),
        ('undersgand', 'understand')
    ]

    successful_assertions = 0

    for input_word, expected_output in test_cases:
        try:
            assert predict(input_word) == expected_output
            successful_assertions += 1
        except AssertionError:
            print(f"Assertion failed for: predict({input_word}) == {expected_output}")
            print(f"Predicted word is == {predict(input_word)}")

    print(f"Number of successful assertions: {successful_assertions}")


@timer
def predict(word):
    sorcerer = Sorcerer(False, "slim")
    return sorcerer.predict(word)

if __name__ == '__main__':
    main()
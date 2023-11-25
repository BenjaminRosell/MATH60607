from project import Sorcerer
from utils import timer

@timer
def main():
    assert predict('newspaler') == 'newspaper'
    assert predict('informagion') == 'information'
    assert predict('backrround') == 'background'
    assert predict('oppodtunity') == 'opportunity'
    assert predict('importnat') == 'important'
    assert predict('marleting') == 'marketing'
    assert predict('protecgion') == 'protection'
    assert predict('produdtion') == 'production'
    # assert predict('develolment') == 'development'
    # assert predict('environnent') == 'environment'
    # assert predict('umiversity') == 'university'
    # assert predict('popukation') == 'population'
    # assert predict('ddpartment') == 'department'
    # assert predict('apqrtment') == 'apartment'
    # assert predict('comnitment') == 'commitment'
    # assert predict('responsivle') == 'responsible'
    # assert predict('discuwsion') == 'discussion'
    # assert predict('spectqcular') == 'spectacular'
    # assert predict('chocplate') == 'chocolate'
    # assert predict('partifular') == 'particular'
    # assert predict('tradigional') == 'traditional'
    # assert predict('diffisulty') == 'difficulty'
    # assert predict('cimmercial') == 'commercial'
    # assert predict('ewucation') == 'education'
    # assert predict('sometying') == 'something'
    # assert predict('operayion') == 'operation'
    # assert predict('journqlist') == 'journalist'
    # assert predict('celebrayion') == 'celebration'
    # assert predict('manafement') == 'management'
    # assert predict('edpecially') == 'especially'
    # assert predict('experirnce') == 'experience'
    # assert predict('relatjonship') == 'relationship'
    # assert predict('conferfnce') == 'conference'
    # assert predict('associstion') == 'association'
    # assert predict('ligerature') == 'literature'
    # assert predict('prdsident') == 'president'
    # assert predict('tecjnology') == 'technology'
    # assert predict('colkection') == 'collection'
    # assert predict('induatrial') == 'industrial'
    # assert predict('difrerence') == 'difference'
    # assert predict('voluntwer') == 'volunteer'
    # assert predict('conmunity') == 'community'
    # assert predict('remaruable') == 'remarkable'
    # assert predict('investmejt') == 'investment'
    # assert predict('succesqful') == 'successful'
    # assert predict('sugrestion') == 'suggestion'
    # assert predict('thriughout') == 'throughout'
    # assert predict('achiebement') == 'achievement'
    # assert predict('sectetary') == 'secretary'
    # assert predict('undersgand') == 'understand'

@timer
def predict(word):
    sorcerer = Sorcerer(False, "slim")
    return sorcerer.predict(word)

if __name__ == '__main__':
    main()
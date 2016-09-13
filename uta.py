# coding: utf-8

import sys
import re
from unicodedata import normalize
from MeCab import Tagger
from number_reader import number_reading

T = Tagger()
NUMBER_PATTERN = re.compile('^[0-9０-９]+$')
NUMBER_DELIMITER_PATTERN = re.compile('^[\.,]$')
HAIKU = [5, 7, 5]
TANKA = [5, 7, 5, 7, 7]
YOMI_DICT = {
  'A': 'エイ',
  'B': 'ビー',
  'C': 'シー',
  'D': 'ディー',
  'E': 'イー',
  'F': 'エフ',
  'G': 'ジー',
  'H': 'エイチ',
  'I': 'アイ',
  'J': 'ジェイ',
  'K': 'ケイ',
  'L': 'エル',
  'M': 'エム',
  'N': 'エヌ',
  'O': 'オウ',
  'P': 'ビー',
  'Q': 'キュー',
  'R': 'アール',
  'S': 'エス',
  'T': 'ティー',
  'U': 'ユー',
  'V': 'ブイ',
  'W': 'ダブリュ',
  'X': 'エックス',
  'Y': 'ワイ',
  'Z': 'ゼット',
  '1': 'イチ',
  '2': 'ニ',
  '3': 'サン',
  '4': 'ヨン',
  '5': 'ゴ',
  '6': 'ロク',
  '7': 'ナナ',
  '8': 'ハチ',
  '9': 'キュウ'
}
for k in list(YOMI_DICT.keys()):
    YOMI_DICT[k.lower()] = YOMI_DICT[k]


def main(sentence, syllable_pattern=TANKA):
    sentence = re.sub('\s+', ' ', sentence.replace('\u3000', ' '))
    parsed_sentence = parse_sentence(sentence)
    collected_uta = list(collect_uta(parsed_sentence, syllable_pattern))
    collected_uta.sort(key=lambda x: x[2], reverse=True)
    return collected_uta


def parse_sentence(sentence):
    """
    文章を受け取り、MeCabで形態素解析して
    (元の綴り, 品詞, 接続, よみがな, 音節の長さ)
    のタプルが入った配列を返す。
    MeCabで正しい読みを取得できない以下のパターンのみ、別の方法で読みを取得する。
      - ローマ字1文字 => YOMI_DICTより読みを取得
      - 数値 => number_readerで読みを取得
    """
    parsed_sentence = []
    number_string = ''

    for line in T.parse(sentence).split('\n'):
        fields = line.split(',')
        if len(fields) < 7:
            continue

        try:
            term, part = fields[0].split('\t')
            detail = fields[1]

            if NUMBER_PATTERN.match(term) or (NUMBER_DELIMITER_PATTERN.match(term) and number_string):
                number_string += term
                continue
            else:
                if number_string:
                    number_tokens = number_reading(number_string.rstrip(',.'))
                    parsed_sentence += [(n[0], n[1], n[2], n[3], syllable_len(n[3])) for n in number_tokens]
                    number_string = ''

            if is_all_katakana(fields[-2]):
                reading = fields[-2]
            elif is_all_katakana(term):
                reading = term
            else:
                reading = YOMI_DICT.get(term, '')

            slen = syllable_len(reading)
            parsed_sentence.append((term, part, detail, reading, slen))

        except:
            continue

    return parsed_sentence


def is_all_katakana(word):
    """単語がカタカナのみで構成されているかどうかを判定する。中黒はカタカナとみなす"""
    for c in word:
        if not ord('ァ') <= ord(c) <= ord('ヿ'):
            return False
    return True


def syllable_len(kana):
    """カタカナの音節の長さを取得する"""
    slen = 0
    for c in kana:
        if c not in ('ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ', '・'):
            slen += 1
    return slen


def collect_uta(parsed_sentence, uta_slen_pattern):
    """
    パース後の文章を受け取り、詩となる可能性のある部分を抽出する。1つの詩を
    (抽出されたフレーズの配列, 読みがなの配列, スコア(大=良))
    の形式で取得し、見つけた時点ですぐyieldする。
    """
    term_num = len(parsed_sentence)

    phrase = ''
    rphrase = ''
    phrase_slen = 0
    phrase_index = 0
    uta = []
    ruta = []
    score = 0

    for i in range(term_num):

        # 詩の先頭となる単語は特定のパターンに絞る
        first_term = parsed_sentence[i]
        if first_term[1] not in ('名詞', '形容詞', '動詞', '副詞') or first_term[2] == '接尾':
            continue

        offset = 0

        while True:
            if i + offset >= term_num:
                break

            term, part, detail, reading, slen = parsed_sentence[i + offset]

            if phrase == '' and detail in ('句点', '読点', '括弧閉'):
                uta[-1] += term
                offset += 1
                continue

            target_phrase_slen = uta_slen_pattern[phrase_index]

            # フレーズの先頭になる単語がひらがな1文字の場合、印象が悪いことが多いのでスコアを落とす
            if phrase == '' and len(term) == 1 and ord('ぁ') <= ord(term) <= ord('ん'):
                score -= 1

            if phrase_slen + slen < target_phrase_slen:
                phrase += term
                rphrase += reading
                phrase_slen += slen

            elif phrase_slen + slen > target_phrase_slen:
                break

            elif reading.endswith('ッ'):
                break

            else:
                uta.append(phrase + term)
                ruta.append(rphrase + reading)
                if len(uta) == len(uta_slen_pattern):
                    yield (uta, ruta, score)
                    break

                phrase_index += 1
                phrase = ''
                rphrase = ''
                phrase_slen = 0

            offset += 1

        phrase = ''
        rphrase = ''
        phrase_slen = 0
        phrase_index = 0
        uta = []
        ruta = []
        score = 0



if __name__ == '__main__':
    txt = sys.argv[1] if len(sys.argv) > 1 else 'sample.txt'
    for uta in parse_sentence(open(txt).read()):
        print(uta)

# coding: utf-8

DECIMAL_DELIMITER = ('.', '記号', '記号', 'テン')
DIGIT_DELIMITER = (',', '記号', '記号', '')
NUMBER_READINGS = ['ゼロ', 'イチ', 'ニ', 'サン', 'ヨン', 'ゴ', 'ロク', 'ナナ', 'ハチ', 'キュウ']
REPEATED_DIGIT_SUFFIXES = ['', 'ジュウ', 'ヒャク', 'セン']
# 兆までの読み方だけに対応
ONETIME_DIGIT_SUFFIXES = ['', 'マン', 'オク', 'チョウ']


def number_reading(numbers):
    split_numbers = numbers.split('.')
    if not (split_numbers[0].startswith('0') and len(split_numbers[0]) > 1):
        if len(split_numbers) == 1:
            return read_int(split_numbers[0])
        elif len(split_numbers) == 2:
            return read_int(split_numbers[0]) + [DECIMAL_DELIMITER] + read_decimal(split_numbers[1])

    readings = read_decimal(split_numbers[0])
    for number_part in split_numbers[1:]:
        readings.append(DECIMAL_DELIMITER)
        readings += read_decimal(number_part)
    return readings


def read_int(numbers):
    if numbers == '0':
        return [('0', '名詞', '数', 'ゼロ')]

    max_digit = len(numbers.replace(',', ''))
    # 桁数が大きすぎる場合は読むのを諦めて空の配列を返す
    if max_digit > len(ONETIME_DIGIT_SUFFIXES) * 4:
        return []

    d = 0
    readings = []
    for i in range(1, len(numbers) + 1):
        c = numbers[-i]
        if c == ',':
            readings.insert(0, DIGIT_DELIMITER)
            continue

        char_reading = '' if c == '0' else NUMBER_READINGS[int(c)]
        if d % 4 == 0:
            suffix = ONETIME_DIGIT_SUFFIXES[int(d / 4)]
        else:
            if c == '1':
                char_reading = ''
            if c == '0':
                suffix = ''
            else:
                suffix = REPEATED_DIGIT_SUFFIXES[int(d % 4)] 

        reading = char_reading + suffix
        readings.insert(0, (c, '名詞', '数', reading))
        d += 1

    return readings
        


def read_decimal(numbers):
     return [(c, '名詞', '数', NUMBER_READINGS[int(c)]) for c in numbers]


if __name__ == '__main__':
    while True:
        for term in number_reading(input()):
            print(term)

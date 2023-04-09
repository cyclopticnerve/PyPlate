def main():

    stra = 'cat1, cat2'
    strb = 'pdep1, pdep2'

    straj = _split_quote(stra, join=';', tail=';')
    strbj = _split_quote(strb, quote='"', lead='\t', join=',<br>\n\t', tail='\n')

    print(straj)
    print(strbj)


def _split_quote(str_in, split=',', quote='', lead='', join=',', tail=''):
    """
        A helper function to split and reformat keywords and dependencies

        Paramaters:
            str_in [string]: the string to split
            split [string]: the character to split on
            quote [string]: the character to use to quote each entry (or empty)
            lead [string]: the string to preceed the formatted string (or empty)
            join [string]: the string to join each line in the output (or empty)
            tail [string]: the string to follow the formatted string (or empty)

        Returns:
            [string]: a new string which is split, quoted, joined, and
            surrounded by the lead and tail strings

        This function takes a string and splits it using the split param, then
        quotes each item using the quote param, then joins the items using the
        join param, and surrounds it using the lead and tail params to create a
        nice-looking list.
    """

    # first split the list using the split char
    split_lst = [item.strip() for item in str_in.split(split)]

    # blank strings, when split w/param, still contain 1 entry
    # https://stackoverflow.com/questions/16645083/when-splitting-an-empty-string-in-python-why-does-split-return-an-empty-list
    # so we do the list comprehension BEFORE testing the list length
    # quote items and put into new list
    split_lst = [f'{quote}{item}{quote}' for item in split_lst if item != '']

    # if the list is empty, return empty result
    if len(split_lst) == 0:
        return ''

    # join list using join string
    split_lst_str = f'{join}'.join(split_lst)

    # surround list with lead and tail
    split_lst_str = f'{lead}{split_lst_str}{tail}'

    # return the final result string
    return split_lst_str


if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    main()

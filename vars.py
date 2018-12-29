data_buffer = {}


def reset_buffer():
    """
    Resets the data buffer to default values
    """
    global data_buffer
    data_buffer = {'Title': "",
                   'Genre': "",
                   'Rated': "",
                   'Type': "",
                   'Format': "",
                   'Year': "",
                   'Runtime': "",
                   'Plot': "",
                   'Metascore': ""}


def __init__():
    reset_buffer()

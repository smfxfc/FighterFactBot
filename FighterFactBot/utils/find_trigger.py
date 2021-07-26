#! python3

trigger = "fighterfact"  # if trigger string is in a comment, bot will execute


def detect_trigger(text):
    """Check input comment string for bot trigger. Return True if trigger exists."""
    return True if trigger in text.lower() else None


def get_trigger_index(text):
    """First step to parsing the fighter name from a user's comment.
    This func gets the index of the 'fighterfact' element within the comment body. This index
    will be used to reference the fighter's name."""

    comment_ls = text.lower().split()  # tranform comment into list of words

    for i, j in enumerate(comment_ls):  # determine list index of each word
        if j == trigger:
            index = i
    return index


def get_fighter(text):
    """Parse user comment and extract fighter name."""

    idx = get_trigger_index(text)

    # the 2 elements following the trigger word are the first, last name of fighter
    end_idx = idx + 3
    comment_ls = text.lower().split()

    # extract target list: [trigger, firstname, lastname]
    target_phrase = comment_ls[idx:end_idx]
    fighter = " ".join(target_phrase[1:])  # combine first and last name of fighter
    return fighter

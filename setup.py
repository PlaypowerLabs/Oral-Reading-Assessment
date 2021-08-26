import random

PASSAGE_LIST = []
PASSAGE_LIST.append('''Opera refers to a dramatic art form, originating in Europe,
in which the emotional content is conveyed to the audience as much through music,
both vocal and instrumental, as it is through the lyrics.''')

PASSAGE_LIST.append('''John went for a bike ride. He rode
around the block. Then he met some girls he knew from school.
They all rode to the field to play. John had a great time playing
games with his friends.''')

PASSAGE_LIST.append("""Tim went to the park with his brother. They
brought baseballs and gloves. They played catch for two hours. It started
to get very hot out, so they went home for some lemonade. They
had a great day.""")

PASSAGE_LIST.append("""The ocean has bright blue water
filled with waves. Many types of fish live in the ocean.
Seagulls love flying over the ocean to look for fish.
There is soft sand along the shore, and there are pretty seashells
in the sand. The ocean is a great place to visit.""")

PASSAGE_LIST.append("""The kids were outside playing catch. They heard a
rumble in the sky. They didn’t want to stop
playing, but they knew it wasn’t safe to be out in
a storm. Also, they did not want to get wet.
They decided to go inside and play a board game.
They loved listening to the thunder as they played their game.
The kids went outside again after the storm had
passed. They saw a rainbow!""")


def get_passage():
    return random.choice(PASSAGE_LIST)
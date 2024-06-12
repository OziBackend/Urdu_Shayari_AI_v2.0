prompts = {
    # To get poetries about "GIVEN POET AND POEM"
    "1": f"""I want to generate {{poet_name}} poetry {{poem_name}} in Urdu text. each stanza on new line. There should be 8 lines or more. Strictly there should be no English. The format should be in following format:['first stanza ',  'second stanza', 'third stanza', 'fourth stanza', 'fifth stanza',......]""",
    # To get poetries about "GIVEN TOPIC"
    "2": f"""I want to generate  'نظمیں' about '{{poetry_topic}}' in Urdu text. Each Poetry seperated by new line. Number of poems should be 6 and each containing 4 sentences or more. Strictly there should be no English. The format should be in following  format:

    [['1st stanza of poem1', '2nd stanza of poem1','3rd stanza of poem1',....],
    ['1st stanza of poem2', '2nd stanza of poem2','3rd stanza of poem2',....],
    ['1st stanza of poem3', '2nd stanza of poem3','3rd stanza of poem3',....],
    ......]""",
    # To get poetries or ghazals or rabayi
    "3": """I want to generate '{{poetry_category}}' in Urdu text. Each Poetry separated by new line. Number of poems should be between 2 and 3 and each containing 4 or more sentences. Strictly there should be no English. The format should be in following  format:

    [['1st stanza of poem1', '2nd stanza of poem1','3rd stanza of poem1',....],
    ['1st stanza of poem2', '2nd stanza of poem2','3rd stanza of poem2',....],
    ['1st stanza of poem3', '2nd stanza of poem3','3rd stanza of poem3',....],
    ......]""",

    # To stream poetries about "GIVEN TOPIC"
    "4": f"""I want to generate  'نظمیں' about '{{poetry_topic}}' in Urdu text. Number of poems should be 4 and each containing 4 sentences or more. Strictly there should be no English text in your response and there should be no useless text other than poems. The format should be in following  format:

        ['1st stanza of poem1', '2nd stanza of poem1','3rd stanza of poem1',....],
        ['1st stanza of poem2', '2nd stanza of poem2','3rd stanza of poem2',....],
        ['1st stanza of poem3', '2nd stanza of poem3','3rd stanza of poem3',....],
        ....""",
    # To stream poetries about "GIVEN TOPIC"
    "5": f"""I want to generate '{{poetry_type}}' in Urdu text. Number of poems should be 4 and each containing 4 sentences or more. Strictly there should be no English text in your response and there should be no useless text other than poems. The format should be in following  format:

        ['1st stanza of poem1', '2nd stanza of poem1','3rd stanza of poem1',....],
        ['1st stanza of poem2', '2nd stanza of poem2','3rd stanza of poem2',....],
        ['1st stanza of poem3', '2nd stanza of poem3','3rd stanza of poem3',....],
        ....""",
}

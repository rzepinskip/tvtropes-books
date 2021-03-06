import pytest

from tvtropes.parser import SpoilerParser


@pytest.fixture(scope="session")
def parser():
    return SpoilerParser()


@pytest.mark.parametrize(
    "raw_example, expected",
    [
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/BloodKnight" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/BloodKnight">Blood Knight</a>: The book contains three of these:<ul><li> Greven il-Vec, as it is said at one point that he only smiles when he is about to kill someone.</li><li> Like all Keldon warriors, Maraxus of Keld is one of these.</li><li> <span class="spoiler" title="you can set spoilers visible by default on your profile">Crovax</span> becomes one of these in the final chapter.</li>
        """,
            [False, False, True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/BornUnlucky" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/BornUnlucky">Born Unlucky</a>: Poor <span class="spoiler" title="you can set spoilers visible by default on your profile">Mirri</span> was doomed practically from the word go, as she was born with different-colored eyes that caused her people to see her as an ill omen and cast her out.
        """,
            [True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/ButtMonkey" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/ButtMonkey">Butt-Monkey</a>: <span class="spoiler" title="you can set spoilers visible by default on your profile"> Mirri</span> does not get a happy ending in this book or <span class="spoiler" title="you can set spoilers visible by default on your profile"> any other for that matter.</span><ul><li> Ertai is also often made one of these, though it doesn't really kick into high gear for him until <em>Nemesis</em>.</li>
        """,
            [True, False],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/Curse" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/Curse">Curse</a>: Selenia apparently carries one, and passes it to <span class="spoiler" title="you can set spoilers visible by default on your profile">Crovax</span> when he kills her.
        """,
            [True],
        ),
        (
            """<a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/DestructiveRomance" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/DestructiveRomance">Destructive Romance</a>: Crovax's obsession with Selenia winds up <span class="spoiler" title="you can set spoilers visible by default on your profile">getting her killed and turning him into a vampire</span>.
        """,
            [True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/EvilIsBigger" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/EvilIsBigger">Evil Is Bigger</a>: Seems to be a recurring theme on Rath.<ul><li> The Predator is almost twice as large a ship as the Weatherlight. <span class="spoiler" title="you can set spoilers visible by default on your profile">Unfortunately it later succumbs to <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/VillainForgotToLevelGrind" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/VillainForgotToLevelGrind">Villain Forgot to Level Grind</a></span>.</li><li> Commander Greven il-Vec, the captain of Predator, is nearly seven feet tall, outfitted from head to toe in Phyrexian exoskeletal armor, and if his card is an accurate depiction of his strength, has a strength surpassing his master Volrath, any of the Weatherlight's heroes, and even the <em>legendary dragons</em> that show up in the <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Literature/InvasionCycle" title="https://tvtropes.org/pmwiki/pmwiki.php/Literature/InvasionCycle">Invasion Cycle</a>.</li>
        """,
            [False, False, True, False],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/EyeScream" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/EyeScream">Eye Scream</a>: Starke is blinded with a sword by his daughter Takara. <span class="spoiler" title="you can set spoilers visible by default on your profile">Or rather, Volrath disguised as Takara</span>.
        """,
            [False, True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/FaceHeelTurn" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/FaceHeelTurn">Face–Heel Turn</a>: Selenia and eventually <span class="spoiler" title="you can set spoilers visible by default on your profile">Crovax</span>.<ul><li> <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/FaceMonsterTurn" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/FaceMonsterTurn">Face–Monster Turn</a>: Selenia is this, though exactly <em>how</em> it happens is unknown. She callously lets Vhati il-Dal fall to his death, leads the Phyrexians to the Weatherlight and attacks the heroes in the Stronghold, but at the last she shows notable reluctance, crying as she fights Crovax.</li>
            """,
            [False, False],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/HeroicSacrifice" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/HeroicSacrifice">Heroic Sacrifice</a>: <span class="spoiler" title="you can set spoilers visible by default on your profile"> Mirri</span> dies in battle with <span class="spoiler" title="you can set spoilers visible by default on your profile">Crovax</span> to protect <span class="spoiler" title="you can set spoilers visible by default on your profile">Gerrard</span>.
        """,
            [True],
        ),
        (
            """<lit><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/IWantMyBelovedToBeHappy" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/IWantMyBelovedToBeHappy">I Want My Beloved to Be Happy</a>: <span class="spoiler" title="you can set spoilers visible by default on your profile"> Mirri</span>.
        """,
            [],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/JustFriends" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/JustFriends">Just Friends</a>: Mirri's Tale reveals that <span class="spoiler" title="you can set spoilers visible by default on your profile">Gerrard feels this way about Mirri, feeling that they are <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/LikeBrotherAndSister" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/LikeBrotherAndSister">Like Brother and Sister</a> and that he cannot reciprocate their love because they are too different</span>.
        """,
            [True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/LoveMartyr" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/LoveMartyr">Love Martyr</a>: <span class="spoiler" title="you can set spoilers visible by default on your profile">Mirri learns during her <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/VisionQuest" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/VisionQuest">Vision Quest</a> that Gerrard can only love her "after his fashion" and that it will never be what she needs, but she decides to stay by him anyway</span>.
        """,
            [True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/LoveTriangle" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/LoveTriangle">Love Triangle</a>: Type 4. <span class="spoiler" title="you can set spoilers visible by default on your profile"> Mirri</span> LOVES Gerrard but he likes her as a friend. <span class="spoiler" title="you can set spoilers visible by default on your profile"> Hanna</span> likes Gerrard, a feeling which is <span class="spoiler" title="you can set spoilers visible by default on your profile"> reciprocated.</span> What makes it all worse is that Gerrard doesn't know <span class="spoiler" title="you can set spoilers visible by default on your profile"> Mirri</span> LOVES him (he learns it in a dream state, but forgets it immediately after).
        """,
            [True, True, True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/SeriesContinuityError" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/SeriesContinuityError">Series Continuity Error</a>: Hanna's mother is briefly mentioned as being dead, however we find out in <em><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Literature/MasqueradeCycle" title="https://tvtropes.org/pmwiki/pmwiki.php/Literature/MasqueradeCycle">Prophecy</a></em> that she's quite alive. <span class="spoiler" title="you can set spoilers visible by default on your profile">Unfortunately, she dies in the same book</span>.<ul><li> During one of the interludes Tolaria is mentioned to still exist, however in the <a class="createlink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/InvasionCycle" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/InvasionCycle">Invasion Cycle</a> Barrin destroyed the island with the <a class="urllink" href="http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&amp;multiverseid=23098">Oblierate<img src="https://static.tvtropes.org/pmwiki/pub/external_link.gif" style="border:none;" width="12" height="12"></a> spell.</li>
        """,
            [False, True, False],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/ShapeShifterShowdown" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/ShapeShifterShowdown">Shape Shifter Showdown</a>: Played with late in the book with the final battle of <em>Exodus</em>, which is seemingly Gerrard vs Volrath and Starke vs a mind-controlled Takara. <span class="spoiler" title="you can set spoilers visible by default on your profile">"Volrath" is actually a shapeshifting stunt double, while "Takara" is actually the real Volrath in disguise</span>.
        """,
            [False, True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger">The Stinger</a>: The very last pages recount the literary example of one, with the only librarian reading the scene depicted on the card <a class="urllink" href="http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&amp;multiverseid=6076">Mind Over Matter<img src="https://static.tvtropes.org/pmwiki/pub/external_link.gif" style="border:none;" width="12" height="12"></a> (which was <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger">The Stinger</a> for the card set too) where Lyna is shown observing the Weatherlight's escape with <span class="spoiler" title="you can set spoilers visible by default on your profile">Urza</span>. This was a <em>huge</em> deal at the time, as <span class="spoiler" title="you can set spoilers visible by default on your profile">Urza</span> had hitherto been a prerevisionist character that was almost a complete cipher. He would go on to become arguably <strong>the</strong> main character of the Weatherlight Saga.</li>
        """,
            [True, True, False],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/StuffedIntoTheFridge" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/StuffedIntoTheFridge">Stuffed into the Fridge</a>: The between chapters scene right before Mirri's Tale all but says outright that <span class="spoiler" title="you can set spoilers visible by default on your profile">Mirri had to die in order for Gerrard to "shed" her and become a hero</span>, so not only playing this trope as straight as possible but even <em>referencing it in-universe</em>.</li>
        """,
            [True],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/UndyingLoyalty" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/UndyingLoyalty">Undying Loyalty</a>: Tragically subverted, as <span class="spoiler" title="you can set spoilers visible by default on your profile">Mirri does in fact die for her loyalty to Gerrard</span>.
        """,
            [True],
        ),
        (
            """<li> <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/SoBeautifulItsACurse" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/SoBeautifulItsACurse">So Beautiful, It's a Curse</a>: one cause for Emer's ordeal.</li>
        """,
            [],
        ),
        (
            """<li><a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/BadBoss" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/BadBoss">Bad Boss</a>: Volrath is one to Greven. As this card-only quote puts it:<div class="indent"> <strong>Volrath:</strong> There's very little that escapes me, Greven. And you will escape very little if you fail.</div></li>
        """,
            [False, False],
        ),
        (
            """<li> <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/AristocratsAreEvil" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/AristocratsAreEvil">Aristocrats Are Evil</a>: Subverted with Crovax, at least initially...</li>
        """,
            [False],
        ),
    ],
)
def test_cleaning(parser, raw_example, expected):
    _, sentences = parser.parse(raw_example)
    results = [tag for tag, _, _ in sentences]
    if results != expected:
        raw_example = raw_example.replace("\n", "")
        print(f"RAW: {raw_example}")
        cleaned_example = " ".join([sentence for _, sentence, _ in sentences])
        print(f"CLEANED: {cleaned_example}\n")
        for tag, sentence, _ in sentences:
            if tag:
                print(f"SPOILER: {sentence}")
            else:
                print(f"NORMAL: {sentence}")
    assert results == expected


@pytest.mark.parametrize(
    "example, expected",
    [
        ("He killed her. Eddie was a hero.", ["He killed her.", "Eddie was a hero."]),
        ("He, in fact, was a Mr. Monroe.", ["He, in fact, was a Mr. Monroe."]),
    ],
)
def test_sentences_split(parser, example, expected):
    sentences = parser._split_into_sentences(example)
    assert sentences == expected


@pytest.mark.parametrize(
    "example, expected",
    [
        ("There was no help.", True),
        ("Eddie.", False),
        ("Dies", False),
        ("Subverted.", True),  # Not sure about that
    ],
)
def test_sentence_filtering(parser, example, expected):
    is_valid = parser._is_valid_sentence(example)
    assert is_valid == expected


@pytest.mark.parametrize(
    "example, expected",
    [
        (
            (
                "Alan Wayne killed John Conwey at the start.",
                [True, True, False, True, True, False, False, False],
            ),
            [(0, 10), (18, 29)],
        ),
        (("Alan Wayne is dead.", [True, True, True, True]), [(0, 19)]),
        (("Alan Wayne is John.", [False, False, False, True]), [(14, 19)],),
        (("John.", [True]), [(0, 5)],),
    ],
)
def test_tags_indices(parser, example, expected):
    sentence, tags = example
    indices = parser._tags_to_indices(sentence.split(), tags)
    assert indices == expected


def test_directory_parse(parser):
    results = parser.parse_dir("tests/samples")
    assert len(results) == 131

    documents_with_any_spoiler = sum([x["has_spoiler"] for x in results])
    assert documents_with_any_spoiler == 27

    all_labeled_sentences = [
        sentences for item in results for sentences in item["sentences"]
    ]
    spoiler_sentences = sum(
        [is_spoiler for is_spoiler, sentence, _ in all_labeled_sentences]
    )
    assert spoiler_sentences == 32


def test_filtering_out_spoiler_start(parser):
    raw_example = """<li> <a class="twikilink" href="/pmwiki/pmwiki.php/Main/EmergencyImpersonation" title="/pmwiki/pmwiki.php/Main/EmergencyImpersonation">Emergency Impersonation</a>: <span class="spoiler" title="you can set spoilers visible by default on your profile"> Forge, for Elden. This involves putting a fake birthmark on him, which makes the resemblance close enough to trigger Amber's imprint.</span></li>"""
    trope, sentences = parser.parse(raw_example)
    assert len(sentences) == 1

    sentence = sentences[0]
    assert len(sentence[2]) == 1

    spoiler_indices = sentence[2][0]
    assert spoiler_indices[1] == len(sentence[1])


def test_span_invoked_1(parser):
    raw_example = """<a class="twikilink" href="/pmwiki/pmwiki.php/Main/WhatDoYouMeanItsForKids" title="/pmwiki/pmwiki.php/Main/WhatDoYouMeanItsForKids">What Do You Mean, It's for Kids?</a>: <span style="display:none">invoked</span> The <em>Istorii Sankt'ya</em> is a book of religious stories for children which contains extremely graphic illustrations of saints being martyred."""
    trope, sentences = parser.parse(raw_example)
    assert len(sentences) == 1
    assert sentences[0][0] == False


def test_span_invoked_2(parser):
    raw_example = """<li> <a class="twikilink" href="/pmwiki/pmwiki.php/Main/GettingCrapPastTheRadar" title="/pmwiki/pmwiki.php/Main/GettingCrapPastTheRadar">Getting Crap Past the Radar</a>: <span style="display:none">invoked</span> In at least one book, Wally describes how lazy his older brothers are to the point that Wally surmises that they don't even leave the couch to go to the bathroom. It's after this observation that Wally then recalls seeing a garden hose going from said couch to the bathroom. <a class="twikilink" href="/pmwiki/pmwiki.php/Main/Squick" title="/pmwiki/pmwiki.php/Main/Squick">Try not to think too hard about the implications of that.</a></li>"""
    trope, sentences = parser.parse(raw_example)
    assert len(sentences) == 3
    assert all([not is_spoiler for is_spoiler, _, _ in sentences])


def test_spoiler_in_trope(parser):
    raw_example = """<span class="spoiler" title="you can set spoilers visible by default on your profile"><a class="twikilink" href="/pmwiki/pmwiki.php/Main/DownerEnding" title="/pmwiki/pmwiki.php/Main/DownerEnding">Downer Ending</a>: The <a class="twikilink" href="/pmwiki/pmwiki.php/Main/DeusExMachina" title="/pmwiki/pmwiki.php/Main/DeusExMachina">Deus ex Machina</a> is not present in the film version and it's strongly implied that the two protagonists die by drowning.</span>"""
    trope, sentences = parser.parse(raw_example)
    assert len(sentences) == 1
    assert len(sentences[0][2]) == 1


def test_span_notelabel(parser):
    raw_example = """<li> <a class="twikilink" href="/pmwiki/pmwiki.php/Main/TheAlcoholic" title="/pmwiki/pmwiki.php/Main/TheAlcoholic">The Alcoholic</a>: August used to be one and struggles to keep that vice in his past.<span class="notelabel" onclick="togglenote('note0khrd');" style="cursor: pointer;"><sup>*&nbsp;</sup></span><span id="note0khrd" class="inlinefolder font-s" isnote="true" onclick="togglenote('note0khrd');" style="display: none; cursor: pointer;">Disregarding a couple of <a class="twikilink" href="/pmwiki/pmwiki.php/Main/SeriesContinuityError" title="/pmwiki/pmwiki.php/Main/SeriesContinuityError">continuity errors</a> in the early chapters.</span> So he's picked up a <a class="twikilink" href="/pmwiki/pmwiki.php/Main/MustHaveNicotine" title="/pmwiki/pmwiki.php/Main/MustHaveNicotine">different habit</a> to use as an emotional crutch instead.</li>"""
    trope, sentences = parser.parse(raw_example)
    assert len(sentences) == 1
    assert all([not is_spoiler for is_spoiler, _, _ in sentences])

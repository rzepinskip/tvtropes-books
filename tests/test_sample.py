from tvtropes.parser import parse
from lxml import etree


def test_single_list():
    example = (
        """
        <li> <span class="spoiler">Alia marries Duncan Idaho</span> when she is only fifteen. His age is a little murky because he died in the first book and was cloned, quite possibly artificially aged, but he was definitely an adult <span class="spoiler" title="x">after he regained his memories</span>. This marriage serves to reinforce the idea that Alia's flesh is only fifteen, but her experience is ancient.</li>
        """,
    )
    tree = etree.XML(example[0])
    parse(tree)


def test_nested_list():
    example = (
        """<li> <a class="twikilink" href="x" title="x">Contrived Coincidence</a>: Some sentence:
    <ul>
        <li> <span class="spoiler" title="x">Had the climax not
                occurred on a night with a full moon, Pettigrew would have been arrested and Sirius cleared, completely
                changing the arc of the next four books. Lupin probably would have also remained teacher, since Snape
                wouldn't have found Sirius while trying to bring Lupin his Wolfsbane Potion and ultimately outed Lupin
                as a werewolf out of spite. This is especially funny when it's revealed, <a class="twikilink"
                title="x">three books later</a>, that Voldemort cursed the Defence Against the Dark Arts position.
                So with this curse Voldemort was ultimately able to make a new body.</span></li>
        <li> <span class="spoiler" title="x">The only reason that
                Sirius even breaks out of Azkaban in the first place is that: (A) the Weasleys win the wizard lottery;
                (B) this is apparently front-page news; (C) Ron has Scabbers in the picture; and (D) Cornelius Fudge
                just happens to be carrying that exact issue of the <em>Daily Prophet</em> when he visits Black's
                cell.</span></li>
        <li> Harry just happens to get his hands on the Marauder's Map the 
        very same year that one of its creators is teaching at Hogwarts. 
        <span class="spoiler" title="x">The other three were his own departed
        father, Ron's rat, and lastly, the eponymous prisoner of Azkaban.</span></li>
        </ul>
    </li>""",
    )
    tree = etree.XML(example[0])
    parse(tree)


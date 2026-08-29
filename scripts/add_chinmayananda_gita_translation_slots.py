#!/usr/bin/env python3
"""Add bidirectional Sanskrit↔English slots to Chinmayananda's Gītā quotes.

The markup changes no wording. Each English phrase remains exactly the
scan-backed Chinmayananda translation and points to the Sanskrit word indices
that it renders. Multi-word interpretive phrases deliberately point to all
relevant Sanskrit words rather than pretending to be one-word glosses.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "gita/vishnu-sahasranama/commentary-quote-analysis.json"

SLOTS = {
    "name-12-paragraph-1-span-0": "{0,1:There where having gone}, {2,3:men never return}. {4,5,6,7:That sacred place is My seat}",
    "name-12-paragraph-2-span-0": "{3:O Son of Kunti}, {0,1:having reached Me}, {2,4,5,6,7:there shall be no more any re-birth}",
    "name-12-paragraph-2-span-1": "{0,1:That having reached} {2,3,4:no return again}",
    "name-19-paragraph-1-span-0": "{0,1,2,3,4,5,6:Those who contemplate upon Me with total dedication}, {7,8,9,10,11:their daily welfare and spiritual progress} {12,13:I shall bear}",
    "name-28-paragraph-1-span-0": "{0:Eternal}, {1,2:All — Pervading}, {3:the Pillar}, {4:Motionless} {5,6:(is) this Ancient One}",
    "name-95-paragraph-0-span-0": "{0:That which is born} {1,2:must necessarily} {3:die}",
    "name-107-paragraph-1-span-1": "{0,3,4:I am the Seer} {1,2:in} {5,6,7:all the fields-of-experiences everywhere}",
    "name-114-paragraph-0-span-3": "{0:Among the Rudras}, {2,3:I am} {1:Śaṅkara}",
    "name-118-paragraph-0-span-0": "{0:Everywhere} {1:are His ears}",
    "name-124-paragraph-0-span-0": "{3:The Light} {1,2,4,5,6:that illumines} {0:all lights}",
    "name-129-paragraph-0-span-0": "{1,3,5,6:This great Reality is} {0:Imperceptible}, {2:Unthinkable}, {4:without any modifications}",
    "name-133-paragraph-1-span-0": "{13,14:The Supreme puruṣa} {11,12:in this body} {7,8,9,10:is also called} {0:the spectator}, {1:the permitter}, {2,3:the supporter}, {4:the enjoyer}, {5:the great Lord}, {6:and the Supreme Self}",
    "name-147-paragraph-1-span-0": "{0:Among the Pandavas}, {1:I am Arjuna}",
    "name-170-paragraph-2-span-0": "{2:Very difficult indeed it is to cross over} {0,1:My māyā}",
    "name-189-paragraph-0-span-0": "{2:I am} {0:the Light} {1:in all effulgents}",
    "name-193-paragraph-0-span-0": "{3:Among the serpents} {1,2:I am} {0:Ananta}",
    "name-200-paragraph-1-span-0": "{0:Among the animals}, {1,3:I am} {2:the King of animals, Lion}",
    "name-228-paragraph-1-span-0": "{5:O Arjuna}, {0:the Lord} {6:dwells} {3,4:in the heart} {1,2:of all}, {7:and spins}. {12:through His māyā}, {8,9:all layers of personal ties} {10,11:as though the universe is a complicated machinery}",
    "name-232-paragraph-1-span-0": "{13:Please understand that} {14:I am} {0,1,2:the Light of the Sun} {3,4,5:that illumines all earth}; {9:and} {6,7:the light and heat in the moon} {8,10:and fire} {11,12,14:are all mine only}",
    "name-236-paragraph-1-span-0": "{0,1,2,3,8,9,12:With a little am I satisfied}. {4,5,7:if it is given} {6,10,11:with sincerity}, {13,14:and with faithful consistency}",
    "name-263-paragraph-1-span-0": "{0,1,2,3:They are in me}; {4,5,6,7,8:I am not in them}",
    "name-275-paragraph-2-span-0-piece-0": "{3:I am} {0:the Might} {1,2:in all strength}",
    "name-275-paragraph-2-span-0-piece-1": "{2:I am} {0:the Brilliancy} {1:in all that is brilliant}",
    "name-279-paragraph-1-span-0": "{7:One who} {0,1,2,3,4:chants my name Om} {8,9,10:and leaves his body at the time of death} {5,6:thus remembering Me}, {11,12,13,14:he shall go to the Supreme State}",
    "name-281-paragraph-1-span-0": "{4,5:As the rays of the moon (Soma)} {0:I fill} {2,3:the vegetable kingdom} {1:with} {6,7:nutrition}",
    "name-285-paragraph-1-span-0": "{11,12:that} {7:nourishes} {13,14:with essence} {8,9,10:all plant kingdom}",
    "name-384-paragraph-2-span-0": "{2:The intellect} {5,6:of one who is practising Yoga} {0,1,3,4:is single-pointed without vacillation}",
    "name-384-paragraph-3-span-0": "{0,1,2:Those who are revelling in sensuality} {3,4,5:and consequently disturbing the poise of their intellect}, {9,10,11:cannot have} {6,7,8:a steady mind} {9:and consistent pursuit of Yoga}",
    "name-391-paragraph-2-span-0": "{9,12:I accept} {4,5,7:even if you offer} {0:some leaf} {1:or flower}, {2:or fruit} {3:or spoon of water}, {13,14:happily}, {6,8,10,11:if it is offered in love}",
    "name-418-paragraph-2-span-0": "{2:I am} {0:the Time} {1:of counting}",
    "name-436-paragraph-1-span-0": "{2,3:This space} {0,1:between earth and the heavens} {9:and} {8,10:all the quarters} {4,5:are filled} {6,7:by You alone}",
    "name-439-paragraph-1-span-0": "{0,1:offer is Brahman}, {2,3:what is offered is Brahman}, {4,5:the fire is Brahman}, {6,7:the offerer is Brahman} {8,9,10,11,12,13,14:and the goal reached is also Brahman}",
    "name-441-paragraph-1-span-0": "{9:among the stars} {8,10:I am} {11:the moon}",
    "name-475-paragraph-1-span-0": "{9,10:In every cycle} {8:I shall manifest} {5,6,7:for re-establishing dharma}",
    "name-479-paragraph-1-span-0": "{9:Arjuna}, {8:I am at once} {0:immortality} {1,2:and} {3:mortality}; {8:I am both} {5:Existence} {4,7:and} {6:Non-existence}",
    "name-481-paragraph-1-span-0": "{1,2:all creatures together} {0:constitute the kṣara-purusha} {3:and the Changeless in all creatures} {5:is} {4:the A-kshara-purusha}",
    "name-517-paragraph-1-span-0": "{0:Of the lakes} {1:I am} {2:the ocean}",
    "name-554-paragraph-1-span-0": "{11,12:understand} {0,1,2,3,4,5,6,7,8,9,10:them all} {16:as coming out} {13,14,15:of my glory}",
    "name-576-paragraph-1-span-0": "{0:Of Vedas} {3:I am} {1,2:the sāma Veda}",
    "name-585-paragraph-1-span-0": "{0,1:To which having gone} {2,3:they return not}; {4:that is} {7:My} {6:Supreme} {5:Abode}",
    "name-599-paragraph-1-span-0": "{5,6:I shall govern} {3,4:both your 'Yoga' and 'kṣema'} {0,1,2:when you are a true devotee}",
    "name-623-paragraph-1-span-0": "{0,1:I am firm}; {2,3:my doubts are gone}. {4:I will do} {5,6:according to your word}",
    "name-632-paragraph-1-span-0": "{0:To them} {1,6:I shall be}, {7:err long}, {2:a Saviour} {3,4,5:from the Ocean of Samsar}",
    "name-657-paragraph-1-span-0": "{6,7:By Thee alone} {4,5:is filled} {1:the earth}, {0,2,3:the outer space and the inner space}. {6:It is Thee who fills} {8,9,10:all directions everywhere}",
    "name-660-paragraph-1-span-0": "{1:I am Dhananjaya}, {0:among the sons of Pandu}",
    "name-673-paragraph-4-span-0": "{1,2,5,6:The Supreme is} {3:the Light} {0:of all lights}, {4:beyond all darkness}",
    "name-673-paragraph-5-span-0": "{13:Understand} {2,11,12,14:that Light} {0,1:in the Sun} {3,4,5:by which the whole world is illumined}, {9:and} {6,7:that Light in the Moon} {8,10:and in the fire} {11,12,14:to be My own Light}",
    "name-677-paragraph-1-span-0": "{3:I am} {0:among the yajñas}, {1,2:the Japa-yajña}",
    "name-678-paragraph-1-span-0": "{6,7:We offer} {0,1:to Brahman} {2,3:that which is Brahman}, {4,5:in the fire which is Brahman}, {6,7:and the act of offering is also Brahman}",
    "name-683-paragraph-1-span-0": "{0:He is the one} {2:dear} {1:to Me}",
    "name-695-paragraph-3-span-0": "{1,2:The Lord dwells in the hearts of all beings}, {0:O Arjuna}, {0,1,2:causing all beings}, {5:by His illusive power}, {0:to revolve} {3,4:as if mounted on a machine}",
    "name-696-paragraph-2-span-0": "{0:I am} {1:the beginning}, {2,3:the middle} {4,7,8:and also} {6:the end} {5:of all beings}",
    "name-698-paragraph-1-span-0": "{2,3,6,7:the oblations are} {0,1,4,5:nothing but Brahman}",
    "name-706-paragraph-1-span-0": "{0,1:My devotee} {2,3:thus knowing (realising the Truth, the jneyam, seated in the heart of all)} {4,5,6:enters into My Being}",
    "name-708-paragraph-2-span-0": "{0:I am} {2:the Source} {1:of all Creation}",
    "name-711-paragraph-1-span-0": "{2,3,4:Of My Divine Glories} {0,1:there is no end}",
    "name-715-paragraph-2-span-0": "{0,1:Greater is their trouble} {2,3,4,5:whose minds are set on the Unmanifest}; {0,1:for the goal, the Unmanifested, is very hard} {2:for the embodied to reach}",
    "name-719-paragraph-1-span-0": "{3:If the splendour} {1,2:of a thousand Suns} {3,4,5:were to blaze out at once} {0:in the sky}, {1,2,3,4,5:that would be like the splendour of that Mighty Being}",
    "name-724-paragraph-1-span-0": "{0,1,2:Hands and feet everywhere}, {4,5,6,7:with heads and mouths everywhere}, {8,9:His ears everywhere}, {3,13:stands} {3:(The Lord)}, {10,11,12:enveloping all}",
    "name-731-paragraph-1-span-0": "{0,1,2:'Om Tat Sat'} {3,4,7:this has been declared to be} {6:the triple designation} {5:of Brahman}",
    "name-732-paragraph-1-span-0": "{1,2:The Unequalled State of Perfection}: {0,1,2:The Supreme State of Truth}",
    "name-742-paragraph-3-span-0": "{0,1,2,3:None there exists who is equal to You}; {4,5,6:how can there be then another superior to You} {0,1,2,3,4,5,6:in the three worlds, O Being of unequalled power}",
    "name-771-paragraph-1-span-0": "{2,3,4,5,6:I am verily that which has to be known in all the Vedas}: {0,1,6:I am indeed the author of the Vedas} {2,3,4,5,6:and the 'knower' of the Vedas am I}",
    "name-772-paragraph-1-span-0": "{2,3,7:The whole universe} {0,6:is supported} {4,5:by one part} {1:of Myself}",
    "name-780-paragraph-2-span-0": "{0,1,2,5:This Yoga of equanimity}, {3,4:taught by Thee}, {6:O slayer of Madhu}, {8,9,10:I see not} {7,13,14:its enduring continuity}, {11,12:because of the restlessness} {11,12:(of the mind)}",
    "name-780-paragraph-3-span-0": "{0:As} {1:a lamp} {2,3:placed in a windless place} {4,5:does not flicker}",
    "name-789-paragraph-1-span-0": "{6,7,12:I am the author} {0,1,2:of all the Vedas}; {3,4,5,8,9,10,11,12:I alone am the knower of the Veda}",
    "name-801-paragraph-1-span-0": "{12,13,14:He attains Peace} {7,8,9,10,11:into whom all desires enter} {6:as} {4,5:waters enter} {3:the ocean}, {0:which filled from all sides}, {1,2:remains unmoved}; {15,16,17:but not the 'desirer-of-desires'}",
    "name-804-paragraph-1-span-0": "{0,1:My māyā (non-apprehension and the consequent misapprehension)} {2:is very difficult to cross over}",
    "name-817-paragraph-1-span-0": "{9,10:I am easily attainable} {8,12,13,14:by that ever-steadfast Yogi} {4,3,6,5,7:who constantly remembers Me daily}, {0,1,2:not thinking of anything else}, {11:O Partha}",
    "name-832-paragraph-1-span-0": "{1:Nourisher} {0,2,3:of All}",
    "name-835-paragraph-1-span-0": "{1,2,4:I am seated} {3:in the heart} {0:of all}—{0,3,4:as the core or Essence in all}",
    "name-859-paragraph-1-span-0": "{1:Among punishers} {2:I am} {0:the Sceptre}",
    "name-877-paragraph-1-span-0": "{3:The Light} {0,1,2:of all lights}",
    "name-892-paragraph-1-span-0": "{0,1:There is neither anything that I have not gained} {0,2:nor anything I have yet to gain}",
    "name-898-paragraph-1-span-0": "{1:I am Kapila} {0,2:among the great ones}",
    "name-915-paragraph-2-span-0": "{0,1,2,3,4,5,6,7:Wherever, there is any special glory in anyone}. {11,12:know} {8,9,10:that} {16:to be a manifestation} {13,14,15:of a part of my Splendour}",
    "name-928-paragraph-1-span-0": "{0,1:For the protection of the good}, {2,4:the destruction of the wicked} {3:and} {5,6,7:the establishment of righteousness}, {8,9,10:He takes different Incarnations}",
    "name-930-paragraph-1-span-0": "{0,1:Permeating the earth} {4,5:I support} {2,3:all beings} {6:by (My) energy}; {8:and} {11,12,13,14:having become the juicy Moon} {7:I nourish} {9,10:all herbs}",
    "name-946-paragraph-1-span-0": "{0,1:Thou art the Father} {2:of the world}, {3:movable and immovable}",
    "name-948-paragraph-1-span-0": "{9:Oh, Glorious Sir}, {0,1,2,3,4,5:seeing your wonderful but awesome form}, {6,7,8:the whole world is shuddering with fear}",
    "name-948-paragraph-2-span-0": "{17:Having seen} {2:Thy} {0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16:Immeasurable Form…} {18,19:the worlds are terrified}, {20,21:and so am I}",
    "name-948-paragraph-3-span-0": "{10,11,12:On seeing Thee} {0,1,2,3,4,5,6,7,8,9:touching the sky…} {13,14:my heart is stricken with dread} {15,16,17:and I find no courage} {18,19:nor peace}, {20:O Viṣṇu}",
    "name-966-paragraph-1-span-0": "{6:He} {0,1:is not born}, {3:nor} {2,4:does He ever die}; {7,8:after having been He again ceases} {5,9,10,11:not to be}; {12:unborn}, {13:eternal}, {14:changeless} {15,16:and ancient} {17,18:he is not killed} {19,20:when the body is killed}",
    "name-972-paragraph-1-span-0": "{4:The 'Enjoyer'} {5:and} {6:the 'Lord'} {2,3:in all yajñas} {0,1,7,8:am I}",
}

# Chinmayananda prints these Gītā passages without a separable English
# translation in the corresponding Sahasranāma entry. The site supplies a
# literal, grammar-aware rendering so the reader retains the same interactive
# Sanskrit↔English UI without attributing unwritten wording to him.
SITE_SLOTS = {
    "name-1-paragraph-2-span-0": "{9,10,11:The self whose mind is joined in yoga} {8:sees} {3:the Self} {0,1,2:abiding in all beings} {6:and} {4,5:all beings} {7:in the Self}; {12,13,14:he sees the same everywhere}",
    "name-81-paragraph-0-span-0": "{0,1,2:Even his taste} {5:turns away} {3,4:upon seeing the Supreme}",
    "name-11-paragraph-4-span-0": "{2:They say} {0,1:the senses are superior}; {4,5:the mind is superior} {3:to the senses}; {7:but} {8,9:the intellect is superior} {6:to the mind}; {13:and} {10,14:that} {12:is beyond} {11:the intellect}",
    "name-31-paragraph-0-span-0": "{0:I manifest} {1,2:age after age}",
    "name-94-paragraph-0-span-1": "{0:With} {1:eyes}, {2:heads}, {3:and faces everywhere}",
    "name-95-paragraph-2-span-0": "{6:This Self} {0,1:is not born}, {3:nor} {2,4:does it ever die}; {7,8:having come to be, it will not} {5,9,10,11:again cease to be}. {12:Unborn}, {13:eternal}, {14:everlasting}, {15,16:and ancient}, {17,18:it is not killed} {19,20:when the body is killed}",
    "name-98-paragraph-1-span-0": "{0,1:Having gone to which} {2,3:they do not return}—{4:that is} {7:My} {6:supreme} {5:abode}",
    "name-104-paragraph-0-span-0": "{0:Among the Vasus} {2,3:I am} {1:Pāvaka}",
    "name-131-paragraph-0-span-0": "{6:I am} {0,1:the maker of Vedānta} {5:and} {2,3,4:indeed the knower of the Veda}",
    "name-132-paragraph-1-span-0": "{0:Among poets}, {1,2:I am Uśanas the poet}",
    "name-143-paragraph-1-span-0": "{3:For} {0:puruṣa}, {1,2:abiding in prakṛti}, {4:experiences} {7:the guṇas} {5,6:born of prakṛti}",
    "name-198-paragraph-0-span-0": "{3:He who} {4:sees} {1,2:the imperishable} {0:amid perishing things}—{5,6:he truly sees}",
    "name-226-paragraph-1-span-0": "{0,1,2:Having many mouths and eyes}, {3,4,5:displaying many wondrous sights}",
    "name-226-paragraph-2-span-0": "{2:Your} {0,1:great form}, {3,4,5:with many mouths and eyes}, {6,7:O mighty-armed one}, {8,9,10,11:with many arms, thighs, and feet}",
    "name-230-paragraph-1-span-0": "{2:Knowledge} {0,1:is covered by ignorance}; {3:by that} {5:beings} {4:are deluded}",
    "name-237-paragraph-1-span-0": "{3:For} {0:puruṣa}, {1,2:abiding in prakṛti}, {4:experiences} {7:the guṇas} {5,6:born of prakṛti}",
    "name-247-paragraph-1-span-0": "{5:I see} {6:You} {0,1,2,3,4:with countless arms, bellies, mouths, and eyes}, {7,8,9:of endless form on every side}. {18:I see} {10,11:no end}, {12,13:no middle}, {14,15,16,17:and no beginning of Yours}, {19:O Lord of the universe}, {20,21:O universal Form}",
    "name-270-paragraph-2-span-1": "{9,10,11:The self whose mind is joined in yoga} {8:sees} {3:the Self} {0,1,2:abiding in all beings} {6:and} {4,5:all beings} {7:in the Self}; {12,13,14:he sees the same everywhere}",
    "name-273-paragraph-2-span-0": "{13:Know} {6,7,8,9,10,11,12:that the light in the moon and in fire}, {0,1,2:and the light abiding in the sun} {3,4,5:that illumines the whole world}, {14:is Mine}",
    "name-274-paragraph-0-span-0": "{0:Just as} {2,6:the one sun} {1:illumines} {5:this} {3,4:whole world}",
    "name-274-paragraph-1-span-0": "{2:so}, {5:O Bhārata}, {1:the knower of the field} {4:illumines} {0,3:the whole field}",
    "name-323-paragraph-1-span-0": "{0:Among lakes} {1:I am} {2:the ocean}",
    "name-359-paragraph-2-span-0": "{1:For} {0:I} {7,8:alone} {4:am the enjoyer} {5:and} {6:Lord} {2,3:of all sacrifices}",
    "name-383-paragraph-2-span-0": "{4,5,6:Veiled by My yogamāyā}, {0,1,2:I am not manifest} {3:to all}",
    "name-389-paragraph-1-span-0": "{1:For} {0:these are divine} {2,3:manifestations of Myself}",
    "name-420-paragraph-1-span-0": "{4:Whoever} {7:offers} {5:to Me} {0:a leaf}, {1:a flower}, {2:a fruit}, {3:or water} {6:with devotion}—{9,12:I accept} {8,10,11:that loving offering} {13,14:from the pure-hearted one}",
    "name-473-paragraph-0-span-0": "{0:Among lakes} {1:I am} {2:the ocean}",
    "name-477-paragraph-1-span-0": "{0,1:For the protection of the good}, {2,4:for the destruction of evildoers}, {3:and} {5,6,7:for the establishment of dharma}, {8:I manifest} {9,10:age after age}",
    "name-478-paragraph-2-span-0": "{3:Know} {1:but} {2:that} {0:to be imperishable} {4:by which} {5,6:all this} {7:is pervaded}",
    "name-505-paragraph-1-span-0": "{1:And}, {4,5,6,7:becoming the essence-filled moon}, {0:I nourish} {2,3:all plants}",
    "name-513-paragraph-1-span-0": "{7:O Bhārata}, {4:know} {1,2,3:Me also} {0:as the knower of the field} {5,6:in every field}",
    "name-531-paragraph-1-span-0": "{0:Among the perfected ones}, {1,2:I am the sage Kapila}",
    "name-555-paragraph-1-span-0": "{5:They speak of} {4,6:the imperishable aśvattha tree} {0,1:with roots above} {2,3:and branches below}",
    "name-625-paragraph-2-span-0": "{3:That has} {0,1,2:hands and feet on every side}, {4,5,6,7:eyes, heads, and faces on every side}",
    "name-633-paragraph-1-span-0": "{2,6:That is said to be} {3:the Light} {0,1:of lights}, {4,5:beyond darkness}",
    "name-666-paragraph-2-span-0": "{6:I am} {0,1:the maker of Vedānta} {5:and} {2,3,4:indeed the knower of the Veda}",
    "name-674-paragraph-0-span-0": "{3:Among nāgas} {1,2:I am} {0:Ananta}",
    "name-674-paragraph-0-span-1": "{0:Among serpents} {1:I am} {2:Vāsuki}",
    "name-695-paragraph-2-span-0": "{5:O Arjuna}, {0:the Lord} {6:dwells} {3,4:in the heart} {1,2:of all beings}",
    "name-696-paragraph-1-span-0": "{2:O Guḍākeśa}, {0,1:I am the Self} {6:abiding} {3,4,5:in the hearts of all beings}",
    "name-745-paragraph-1-span-0": "{5:This Self is} {0:eternal}, {1,2:all-pervading}, {3:stable}, {4:immovable}, {6:and ancient}",
    "name-753-paragraph-1-span-0": "{0:Therefore} {3:Brahman}, {1,2:which pervades all}, {4,6:is ever established} {5:in sacrifice}",
    "name-767-paragraph-1-span-0": "{5:O Arjuna}, {0:the Lord} {6:dwells} {3,4:in the heart} {1,2:of all beings}, {7:causing} {8,9:all beings} {12:by māyā} {7:to revolve} {10,11:as though mounted on a machine}",
    "name-770-paragraph-1-span-0": "{0,1:The fourfold social order} {3:was created} {2:by Me}",
    "name-779-paragraph-2-span-0": "{1:Indeed}, {0,2,5,6:this divine māyā of Mine}, {3,4:consisting of the guṇas}, {7:is difficult to cross}. {10:Those who} {8,9,11:take refuge in Me alone} {14,15:cross beyond} {12,13:this māyā}",
    "name-784-paragraph-1-span-0": "{6:O Dhanañjaya}, {2,3,4,5:there is nothing else} {1:higher} {0:than Me}",
    "name-784-paragraph-2-span-0": "{1,2:All this} {3:is strung} {0:in Me}, {7:like} {5,6:clusters of jewels} {4:on a thread}",
    "name-790-paragraph-1-span-0": "{2:O son of Kuntī}, {5:whatever} {3:forms} {4:arise} {0,1:in all wombs}, {6,7,8,9:the great Brahman is their womb}; {10:I am} {13:the father} {11,12:who gives the seed}",
    "name-816-paragraph-1-span-0": "{3:That has} {0,1,2:hands and feet on every side}, {4,5,6,7:eyes, heads, and faces on every side}",
    "name-824-paragraph-2-span-0": "{1,2:Among all trees} {0:I am the aśvattha}",
    "name-848-paragraph-1-span-0": "{3,4:I alone} {5:am to be known} {0,1,2:through all the Vedas}",
    "name-855-paragraph-1-span-0": "{0,1,2:Its leaves are the Vedic hymns}; {3,4,5:one who knows that tree} {6,7,8:is a knower of the Veda}",
    "name-895-paragraph-1-span-0": "{3:Someone} {2:beholds} {4:this Self} {0,1:as a wonder}; {10,11:another} {7:speaks of it} {5,6:as a wonder} {8,9:in the same way}",
    "name-895-paragraph-2-span-0": "{2:And} {4:another} {5:hears of} {3:this Self} {0,1:as a wonder}; {6,7:even after hearing}, {13:no one} {9:knows} {8,10,11,12:it at all}",
    "name-914-paragraph-1-span-0": "{0,1:What is night} {2,3:for all beings}, {4,5,6:in that the self-controlled one is awake}; {7,8,9:where beings are awake}, {10,11:that is night} {12,13:for the seeing sage}",
    "name-955-paragraph-1-span-0": "{0,1,2:Whatever} {3:the best person does}, {4,5,6:that very thing} {7,8:other people do}",
    "name-977-paragraph-2-span-0": "{0,1:By this you shall prosper}; {2,4:may this be} {3:for you} {5,6,7:the fulfiller of desired aims}",
}

LEGACY_SITE_ENGLISH = {
    "name-81-paragraph-0-span-0": "Rasopyasya Param Drishtvaa Nivartate",
    "name-11-paragraph-4-span-0": "They say the senses are superior; the mind is superior to the senses; but the intellect is superior to the mind; and He is beyond the intellect",
}

SLOT_RE = re.compile(r"\{([\d,\s]+):([^}]*)\}")


def plain(slotted: str) -> str:
    return SLOT_RE.sub(lambda match: match.group(2), slotted)


def indices(slotted: str) -> set[int]:
    return {
        int(value)
        for match in SLOT_RE.finditer(slotted)
        for value in match.group(1).split(",")
        if value.strip()
    }


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    quote_ids = set(data["quotes"])
    if quote_ids != set(SLOTS) | set(SITE_SLOTS) or set(SLOTS) & set(SITE_SLOTS):
        raise ValueError("translation-slot populations do not partition the 142 Gītā blocks")
    untranslated_indices = {}
    for quote_id, slotted in SLOTS.items():
        row = data["quotes"][quote_id]
        if plain(slotted) != row["english"]:
            raise ValueError(f"{quote_id} slot text changes Chinmayananda's wording\nexpected={row['english']!r}\nactual={plain(slotted)!r}")
        expected = set(range(len(row["words"])))
        used = indices(slotted)
        if not used or used - expected:
            raise ValueError(f"{quote_id} Sanskrit coverage mismatch: used={sorted(used)}, expected={sorted(expected)}")
        if expected - used:
            # Chinmayananda sometimes translates only the quoted phrase he is
            # discussing while the block retains the wider canonical line.
            # Do not falsely attach his English to Sanskrit he did not render.
            untranslated_indices[quote_id] = sorted(expected - used)
        row["english_slots"] = slotted
        row["english_source"] = "Swami Chinmayananda"
    for quote_id, slotted in SITE_SLOTS.items():
        row = data["quotes"][quote_id]
        site_english = plain(slotted)
        if row.get("english") not in (None, site_english, LEGACY_SITE_ENGLISH.get(quote_id)):
            raise ValueError(f"{quote_id} unexpectedly has different author English")
        expected = set(range(len(row["words"])))
        used = indices(slotted)
        if used != expected:
            raise ValueError(f"{quote_id} site translation coverage mismatch: missing={sorted(expected-used)}, extra={sorted(used-expected)}")
        row["english"] = site_english
        row["english_slots"] = slotted
        row["english_source"] = "site-literal-translation"
    data["translation_slot_review"] = {
        "translations": len(SLOTS) + len(SITE_SLOTS),
        "chinmayananda_translations": len(SLOTS),
        "site_literal_translations": len(SITE_SLOTS),
        "chinmayananda_wording_changed": False,
        "translated_sanskrit_words_linked": True,
        "untranslated_sanskrit_indices": untranslated_indices,
        "interaction": "bidirectional hover and click through GitaReader",
    }
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["translation_slot_review"], indent=2))


if __name__ == "__main__":
    main()

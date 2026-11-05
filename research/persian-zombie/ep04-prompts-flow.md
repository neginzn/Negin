# قسمت ۴ — پرامپت‌های تصویر (Google Flow) بر اساس اسکریپت v2

## قبل از شروع (مهم برای کیفیت)
- **نسبت تصویر:** 16:9 (Landscape).
- **متن در تصویر نمی‌خواهیم.** همه‌ی نوشته‌ها (اسکن `HUMAN DETECTED`، `DESTINATION: MARS`، HUD، نمایشگر مچ) را من با موشن گرافیک روی تصویر می‌گذارم. برای همین در صحنه‌های نمایشگر، صفحه را خالی و درخشان خواسته‌ام.
- **مرجع‌ها:** کنار هر پرامپت نوشته‌ام کدام عکس‌ها را به‌عنوان ingredient/reference بدهی:
  - `RAY` = hero_reference.png
  - `JAX` = buddy_reference.png
  - `DANIEL` = عکسی که از پرامپت R1 می‌سازی
  - `SUITS` = عکسی که از پرامپت R2 می‌سازی
  - `ALIEN` = همان آدم‌فضایی سبز قسمت ۳
  - `LAB` / `SHUTTLE` = عکس‌هایی که از R3 و R4 می‌سازی
- **هر تصویر را با شماره‌اش ذخیره کن** (`01.png`, `02.png`…) تا روی صدا بچینم.
- اگر یک تصویر خراب شد، فقط همان را دوباره بساز. پرامپت‌ها مستقل‌اند.

**جمله‌ی سبک** (آخر همه‌ی پرامپت‌ها آمده؛ تغییرش نده تا همه یکدست بمانند):
`Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.`

---

## فصل ۰ — مرجع‌ها (اول این‌ها را بساز)

**R1 · Daniel** — مرجع: `RAY` (فقط برای سبک)
```
Character reference sheet of a new stickman character named Daniel, same drawing style as the reference: round white head, thin black stick arms and legs. Daniel is an adult man around 40, short messy brown hair, light stubble, tired kind eyes with dark circles. He wears a worn orange maintenance jumpsuit with grey knee patches, a utility belt and sleeves rolled up. Shown standing in three views: front, three-quarter, side, on a plain light grey background. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, sharp focus, 16:9, no text, no letters, no watermark.
```

**R2 · لباس‌های محافظ** — مرجع: `RAY` + `JAX`
```
Character reference of the two stickmen from the references wearing sleek alien-made protective suits: matte white and silver suits with thin glowing teal seams, flexible joints, a clear round glass bubble helmet, and a small glowing teal display on the left wrist. The grey-cap stickman (Ray) and the black-beanie stickman (Jax) are clearly recognizable through the clear helmets, Ray's grey cap and Jax's black beanie visible inside. Front view, standing side by side on a plain light grey background. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, sharp focus, 16:9, no text, no letters, no watermark.
```

**R3 · آزمایشگاه سفینه (بدون آدم) — نسخه‌ی پیشرفته‌ی روشن را از چت استفاده کن**
```
Interior of an alien spaceship laboratory, no characters. Smooth curved white and pale grey walls, cold white ceiling lights, glowing teal panels, strange organic-looking machines with soft green lights, cables running along the floor, a tall metal storage cabinet, a large sliding door with a round frame. Clean, sterile, eerie, futuristic. Wide shot. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**R4 · داخل شاتل (بدون آدم)**
```
Interior cockpit of a small alien shuttle, no characters. Three curved seats with harness restraints, a wide front window showing black space and stars, a curved control console with glowing teal buttons and three large blank glowing screens, metallic walls with soft white lighting, an emergency storage hatch under the seats. Futuristic, compact, sleek. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۱ — DAY 1

**01** · «You open your eyes.» — مرجع: `RAY`
```
Extreme close-up of the grey-cap stickman's face from the reference, lying on his back, eyes slowly opening, a thin grid of glowing blue laser light reflected in his eyes and across his face, cold white light above. Disoriented, tense. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**02** · «You have thirty days to get off this ship.» — بدون مرجع
```
Exterior view of a colossal alien mothership floating in deep space above Earth, gunmetal grey hull with glowing teal lights, thousands of tiny lit windows, Earth's blue edge curving in the lower corner, stars in the black sky. Epic, ominous, cinematic wide shot. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**03** · «trapped inside a rectangular chamber surrounded by a glowing blue laser field…» — مرجع: `RAY` + `JAX` + `LAB`
```
Wide shot inside the advanced alien laboratory from the reference. In the center, the grey-cap stickman in a navy hoodie from the reference stands inside an empty human-sized rectangular containment field made only of thin bright glowing blue laser beams forming a transparent cage, a glowing emitter pad on the floor and an emitter ring on the ceiling, no booth and no box, he looks around in confusion. In the background on the left, slightly out of focus, the black-beanie stickman in a black tracksuit with a silver chain from the reference sits unconscious on the laboratory chair, wrists and chest strapped with metal restraints, head hanging forward. Bright cold white light, teal accents, floating holographic screens. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```
(قاعده: تا صحنه‌ی ۰۸ هر جا صندلی در قاب است، جکس بسته‌شده رویش باشد. از ۰۹ به بعد صندلی خالی با بندهای باز.)

**04** · «You try to move, but you can't get out.» — مرجع: `RAY`
```
Medium close-up of the grey-cap stickman from the reference pressing both hands against the glowing blue laser beams of an empty transparent laser cage (no booth, no box), small electric sparks flying where his palms touch the field, his face strained and frightened, blue light reflecting on his face. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**05** · «A few meters away, you notice Jax… tied to it.» — مرجع: `JAX` + `LAB`
```
Inside the alien laboratory from the reference, the black-beanie stickman in a black tracksuit with a silver chain from the reference sits unconscious on a cold metal laboratory chair, thick metal restraints around his wrists and a strap across his chest, head hanging forward. A mechanical arm with a small scanner hangs above him. Cold white light from above, long shadows. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**06** · «“Jax!” — He slowly opens his eyes. “Ray…?”» — مرجع: `JAX`
```
Close-up of the black-beanie stickman from the reference strapped to a metal lab chair, slowly lifting his head and opening his eyes, groggy and confused, squinting at the light, blurred blue laser glow of another chamber in the background. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**07** · «…escaping the aliens on Earth. Then a bright light… and nothing.» — مرجع: `RAY` + `JAX`
```
Memory flashback: a dark city street at night, the grey-cap stickman and the black-beanie stickman from the references running away, looking back over their shoulders, a blinding white beam of light from above swallowing them. Slightly faded, desaturated colors with a soft glowing vignette, dreamlike memory feeling. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**08** · «He twists his wrists, trying to create enough space…» — مرجع: `JAX`
```
Tight close-up of the black-beanie stickman's wrists from the reference locked in metal restraints on the armrest of a lab chair, his hand slowly twisting, a small gap of slack visible between the restraint and his wrist, sweat drops, focused effort. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**09** · «…manages to loosen the restraint and pull himself free.» — مرجع: `JAX`
```
Medium shot of the black-beanie stickman from the reference pulling one hand free from the metal restraint of the lab chair, the strap hanging loose, a small triumphant grin on his face, cold white laboratory in the background. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**10** · «He presses the button. The blue laser field disappears.» — مرجع: `RAY` + `JAX`
```
The black-beanie stickman from the reference presses a large glowing button on a control panel beside a rectangular chamber; the blue laser walls of the chamber are fading and breaking apart into small floating particles of light. Inside, the grey-cap stickman from the reference watches in relief. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**11** · «You step out… This isn't a hospital. It's a laboratory.» — مرجع: `RAY` + `JAX` + `LAB`
```
Wide shot inside the alien laboratory from the reference. The grey-cap stickman steps out of an empty chamber frame, weak and unsteady, one hand on the frame, while the black-beanie stickman supports him. Both look around at the strange machines, glowing panels, and cables. Eerie and sterile. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**12** · «Outside, strange figures move through the corridors.» — مرجع: `LAB` + `RAY` + `JAX` + `alien_ref_halfbody.png`
```
Same advanced alien laboratory from the reference, camera placed behind the two stickmen, over their shoulders, looking toward the large oval door at the back of the lab. The oval door is sliding open with a narrow gap in the middle, bright teal light spilling through the gap onto the glossy white floor. Through the gap we see a long curved white spaceship corridor where two tall green aliens from the reference walk past from left to right, seen in profile, not looking at the lab. In the foreground, the grey-cap stickman in a navy hoodie and the black-beanie stickman in a black tracksuit from the references press their backs against the curved lab wall beside the door, peeking around the edge with wide frightened eyes, holding their breath, half hidden in shadow. Tense and secretive. Use the alien reference only for the alien's design (green skin, big glossy black eyes, thin body), not for the background. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**13** · «You find two protective suits inside a storage cabinet.» — مرجع: `SUITS` + `LAB`
```
Medium shot of an opened tall metal storage cabinet in the alien laboratory; inside hang two sleek matte white and silver protective suits with glowing teal seams and two clear bubble helmets on a shelf above, soft light spilling out of the cabinet. The grey-cap stickman and the black-beanie stickman look at them in surprise. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**14** · «The suits have their own oxygen supply… A small display on your wrist…» — مرجع: `SUITS`
```
Close-up of a gloved hand in a white protective suit, a small glowing teal display on the wrist with simple abstract icons and bars, no readable text, a clear helmet visor reflecting the light in the blurred background. Futuristic, clean. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**15** · «Just then, the laboratory door opens. An alien walks inside.» — مرجع: `ALIEN` + `LAB`
```
Low angle shot of the large round sliding door of the alien laboratory opening; a tall green alien with big black eyes from the reference steps inside, backlit by bright teal corridor light, long shadow stretching across the floor. Menacing. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**16** · «You and Jax immediately hide behind a large metal cabinet. Its eyes move across the room.» — مرجع: `SUITS` + `ALIEN`
```
Side composition: on the left, the two stickmen in white protective suits with bubble helmets from the reference crouch tightly behind a tall metal cabinet, holding their breath; on the right, the tall green alien from the reference stands in the middle of the lab, its big black eyes glowing with a faint green scanning light that sweeps across the room. Tense silence. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**17** · «Jax's elbow is sticking out… you pull his arm back.» — مرجع: `SUITS`
```
Tight close-up at the edge of a tall metal cabinet: an elbow in a white protective suit sticks out past the cabinet's edge into a faint green scanning light, and a second gloved hand is reaching to pull it back behind the metal. Extreme tension, shallow depth of field. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**18** · «…continues walking. You don't move until the door closes.» — مرجع: `ALIEN` + `SUITS`
```
Wide shot of the alien laboratory: the tall green alien from the reference walks away toward the far door, its back turned; in the foreground, partially hidden behind a cabinet, the two suited stickmen from the reference stay frozen, eyes wide, watching it leave. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۲ — DAY 2 و DAY 3

(سکانس جدید: کارت روز ۲، آب در بخش خنک‌کننده‌ی سفینه در روز ۳)

### DAY 2

**19** · «AIR: BREATHABLE. You take off your helmets.» — مرجع: Edit روی عکس آزمایشگاه (همان جایی که ایستاده‌اند) + `SUITS`
```
Keep the laboratory and the two stickmen exactly the same, same place and camera angle. Only change this: both stickmen take off their clear bubble helmets and hold them under their arms, taking a deep relieved breath, the grey cap and the black beanie now fully visible. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**20** · «Near a workstation, you find an identification card.» — مرجع: `LAB` + `RAY` + `SUITS`
```
Use the laboratory reference only for the room design, materials, colors and lighting, but show a new close camera angle at one of the sleek white workstations of the same lab. A thin glowing translucent card with a strange alien symbol lies on the desk next to floating holographic teal screens. The grey-cap stickman wearing the spacesuit from the suit reference, helmet off, picks it up with his gloved hand, curious. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**21** · «You hold it against the scanner beside the lab door. The door responds.» — مرجع: Edit روی عکس آزمایشگاه اول
```
Keep the laboratory exactly the same, same camera angle. Only change this: the grey-cap stickman in his spacesuit, helmet off, stands at the large oval door at the back and holds a glowing translucent card against a small round scanner beside the door; the scanner ring glows green and the door has opened a few centimeters, a thin line of light in the middle. The black-beanie stickman in his spacesuit stands behind him, watching. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**22** · «But there's a bigger problem. There's no water in this laboratory.» — مرجع: `RAY` + `JAX` + `SUITS`
```
Medium shot of the two stickmen in spacesuits with helmets off sitting on the glossy white floor of the bright alien laboratory, leaning against a white machine, exhausted and thirsty, the black-beanie stickman holding an empty clear bottle upside down, not a drop left, the grey-cap stickman staring at it. Soft cold light. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

### DAY 3

**23** · «You have to leave the laboratory. …a narrow side corridor.» — مرجع: `RAY` + `JAX` + `SUITS`
```
A narrow quiet side corridor of the alien spaceship, darker and tighter than the laboratory: low curved ceiling, soft dim blue floor lights, smooth grey wall panels with thin glowing seams, small maintenance hatches and bundled cables running along the walls. The two stickmen in spacesuits with helmets off sneak along the wall in a crouch, the grey-cap stickman in front holding the glowing card. Quiet, tense, claustrophobic. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**24** · «Above the main corridor, you notice… A security camera.» — مرجع: `RAY` + `JAX` + `SUITS`
```
View from the end of the narrow dark side corridor looking out into a wide, brightly lit main corridor of the alien spaceship; on its high ceiling a sleek black security camera dome with a small glowing red light slowly turns. In the foreground, the two stickmen in spacesuits press their backs against the side corridor wall, peeking out carefully, staying in the shadow. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**25** · «…the air gets colder. You enter a cooling section…» — مرجع: بدون مرجع شخصیت (یا `RAY` + `JAX` + `SUITS` اگر می‌خواهی در قاب باشند)
```
Wide establishing shot of a cooling section inside the alien spaceship, a completely different look from the laboratory: a large dim industrial hall bathed in cold deep blue light, rows of tall humming cylindrical cooling machines, thick frosted pipes covered in white frost running along the walls and ceiling, cold mist drifting near the floor, small blue indicator lights, metal grated walkways. Advanced but heavy and mechanical. Cold, eerie, beautiful. The two small stickmen in spacesuits enter from a doorway on the left, their breath visible in the cold air. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**26** · «Behind one of the machines, you find a tank of clean water… About twenty liters.» — مرجع: `RAY` + `JAX` + `SUITS` + تصویر ۲۵
```
In the same cold blue cooling section from the reference, behind one of the tall humming cooling machines: a transparent cylindrical water tank about waist height, connected to frosted pipes, full of clean clear water, a small metal valve at the bottom. The grey-cap stickman in his spacesuit, helmet off, kneels and fills a clear bottle from the valve; the black-beanie stickman drinks slowly from another bottle, eyes closed with relief. Cold mist, frost on the pipes. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

**27** · «You write these rules down on a piece of paper.» — مرجع: Edit روی عکس آزمایشگاه یا `LAB` + `RAY` + `JAX`
```
Back in the bright alien laboratory: the grey-cap stickman sits on the floor leaning against a white machine, writing a short list on a crumpled piece of paper with a short pencil, two full water bottles beside him; the black-beanie stickman sits next to him, pointing at the paper. Both in spacesuits with helmets off. Quiet, focused. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no flags, no logos, no text, no letters, no watermark.
```

---

## فصل ۳ — DAY 5

**27** · «…a large room behind a locked door. You use the identification card.» — مرجع: `RAY` + `JAX`
```
The grey-cap and black-beanie stickmen from the references, in white protective suits, stand in front of a massive round locked door in a quiet dim section of the ship; Ray holds the glowing card to the scanner, a ring of green light opening around the door edges. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**28** · «Inside, you see rows of transparent capsules. There are humans inside them.» — بدون مرجع
```
Vast dark hall inside an alien spaceship, endless rows of tall transparent glass capsules lit from within by cold blue light, each holding a sleeping stickman human floating peacefully, men and women of different looks, small children in smaller capsules, soft mist at the floor, rows fading into the distance. Haunting, epic, eerie. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**29** · «You and Jax walk between the capsules…» — مرجع: `RAY` + `JAX`
```
The two stickmen from the references, in white protective suits, walk slowly down a narrow aisle between towering rows of glowing blue glass capsules with sleeping humans inside; they look up in shock, small figures compared to the capsules. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**30** · «Then someone moves. A man inside one of the capsules opens his eyes.» — مرجع: `DANIEL`
```
Close-up through the glass of a blue-lit capsule: the stickman Daniel from the reference, in an orange maintenance jumpsuit, floating inside, suddenly opens his eyes wide and presses one hand against the glass from the inside. Tiny bubbles around him. Startling moment. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**31** · «…you manage to release the capsule. The man falls forward, coughing.» — مرجع: `DANIEL` + `RAY` + `JAX`
```
The glass front of a capsule slides open with a burst of mist; the stickman Daniel in an orange jumpsuit from the reference falls forward, coughing, and the black-beanie stickman catches him by the shoulders, while the grey-cap stickman stands at a small glowing control panel beside the capsule. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**32** · «“My name is Daniel.” …abducted eleven days ago… forced him to work…» — مرجع: `DANIEL`
```
Medium shot of the stickman Daniel from the reference sitting on the floor against a capsule, exhausted, wrapped in his orange maintenance jumpsuit, talking with a tired, haunted expression, one hand gesturing. Cold blue capsule light behind him. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**33** · «“Then why were you treated differently?” Nobody has an answer.» — مرجع: `DANIEL` + `RAY` + `JAX`
```
The three stickmen from the references stand together in the capsule hall: Daniel in his orange jumpsuit looks back over his shoulder at the endless rows of capsules, confused; the grey-cap and black-beanie stickmen in white suits look at each other, uneasy, the question hanging in the air. Long shadows, mysterious blue light. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۴ — DAY 8

**34** · «By the morning of the eighth day, the water tank is almost empty.» — مرجع: `RAY`
```
Close-up of the small transparent water tank behind the machine, almost completely empty, only a few drops at the bottom; the grey-cap stickman's hand from the reference holds an empty bottle under the dripping valve. Worried mood, dim light. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**35** · «…sealed ration packages, compressed food blocks, and three containers of drinking water.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
A small alien storage room with tall shelves: sealed silver ration packages, stacked dense beige food blocks wrapped in clear film, and three large transparent water containers on the floor. The three stickmen from the references stand in the doorway, amazed, light spilling in from behind them. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**36** · «The food blocks are dense and dry… about a quarter of what an adult body needs.» — مرجع: `DANIEL`
```
Close-up of a dense dry beige food block in a gloved hand, small crumbs falling, the stickman Daniel from the reference in the background taking a reluctant bite, unimpressed expression. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**37** · «Jax reaches into his pocket. He finds a small chocolate bar.» — مرجع: `JAX`
```
Medium close-up of the black-beanie stickman from the reference, wearing the white protective suit with the helmet off, pulling a small slightly crushed chocolate bar out of his pocket, looking at it with a soft surprised smile. Warm light on the chocolate. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**38** · «Then he breaks it into three pieces.» — مرجع: `JAX` + `RAY` + `DANIEL`
```
The three stickmen from the references sit in a small circle on the floor of the storage room; the black-beanie stickman breaks the chocolate bar into three equal pieces and hands them out, the grey-cap stickman and Daniel smiling for the first time. Warm, human moment in a cold place. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**39** · «Jax puts his piece back in his pocket. “Later.”» — مرجع: `JAX`
```
Close-up of the black-beanie stickman from the reference slipping his small piece of chocolate back into his pocket with a sly little grin and a wink. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**40** · «You start dividing the remaining supplies into daily portions.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
Top-down view of the floor: food blocks and water bottles arranged in neat small groups like daily portions, a piece of paper with a hand-drawn tally list, the three stickmen's hands from the references sorting the supplies carefully. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۵ — DAY 10

**41** · «He removes a few screws and pulls the panel away.» — مرجع: `DANIEL`
```
The stickman Daniel in an orange maintenance jumpsuit from the reference kneels behind a row of humming machines, unscrewing a square metal wall panel with a small tool, screws on the floor, a dark opening behind the panel. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**42** · «A large ventilation fan is running inside… extremely dangerous.» — بدون مرجع
```
View down a narrow rectangular metal ventilation passage full of cables; at the far end a huge industrial fan spins fast, its blades a blur, wind blowing dust toward the viewer, ominous orange light behind the blades. Dangerous and claustrophobic. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**43** · «Daniel points to a control switch. You wait until the fan stops completely.» — مرجع: `DANIEL`
```
The stickman Daniel from the reference flips a heavy lever switch on a wall box; in the background through the vent opening the giant fan's blades are slowing down, blades now clearly visible. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**44** · «Then you crawl through, one at a time.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
Side cutaway view of a narrow dusty ventilation passage: the three stickmen from the references crawl through in a line, one behind the other, past the stopped fan blades, cables along the walls, dust in the air, a small light at the end. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**45** · «Beyond it is the hangar. A shuttle is parked inside… several aliens are guarding it.» — مرجع: `ALIEN`
```
View through a small dirty observation window from inside a vent: a vast alien hangar with a sleek small silver shuttle parked in the center under bright lights, and several tall green aliens from the reference standing guard around it. Hope and danger in one frame. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۶ — DAY 12

**46** · «…you observe the guards from a safe distance.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
The three stickmen from the references lie on their stomachs inside a vent behind a metal grate, peeking down into a corridor through the gaps, their faces striped by shadows, watching silently. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**47** · «During the shift change, the main corridor stays empty for a short time.» — مرجع: `ALIEN`
```
A long curved main corridor of the alien ship: two tall green aliens from the reference walk away in opposite directions, leaving the center of the corridor empty, soft teal light, a camera dome on the ceiling. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**48** · «You write down the times on your paper.» — مرجع: `RAY`
```
Close-up of the grey-cap stickman from the reference writing small marks on his crumpled paper, his glowing wrist display beside the paper, a focused expression, dim vent light. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**49** · «…quietly enter a security room. Several monitors… a map of the lower levels.» — مرجع: `RAY`
```
A dark alien security room: a curved wall of many glowing monitors showing different corridors and rooms of the ship from above, one large central screen showing a simple glowing schematic map of the lower levels; the grey-cap stickman from the reference stands in front of it, lit by the screens. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۷ — DAY 15

**50** · «You reach the power room… Daniel finds the emergency release.» — مرجع: `DANIEL`
```
A huge alien power room full of humming electrical equipment, thick glowing cables and tall control panels; the stickman Daniel from the reference grips a large red emergency lever with both hands, about to pull it. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**51** · «A loud alarm immediately fills the ship. Red lights begin flashing.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
The power room is suddenly bathed in flashing red emergency light; the three stickmen from the references flinch, covering their ears, shocked, long red shadows on the walls. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**52** · «An alien enters the room… Every part of you behind the metal.» — مرجع: `ALIEN` + `RAY` + `JAX`
```
Red-lit power room: a tall green alien from the reference stands in the doorway, eyes glowing with a faint green scanning light; in the foreground the grey-cap and black-beanie stickmen hide completely behind a large machine, knees pulled in, nothing sticking out; Daniel's orange sleeve barely visible behind a cabinet on the other side. Extreme tension. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**53** · «Instead, every corridor door on the lower level locks at once.» — بدون مرجع
```
A long alien corridor in red emergency light: a series of heavy round blast doors slamming shut one after another down the corridor, sparks at the seams, motion lines. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**54** · «The ship is in lockdown. The guards double.» — مرجع: `ALIEN`
```
A wide corridor in red alarm light with twice as many tall green aliens from the reference walking in formation, searching, their eyes glowing. Threatening. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**55** · «…you hide inside the maintenance passage… drinking only when you have to.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
Inside the narrow dusty vent passage, the three exhausted stickmen from the references sit hunched together, sharing a single almost-empty water bottle, tiny sips, red alarm light flickering through a grate. Weak, tired, determined. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۸ — DAY 18

**56** · «On the third day, the alarm finally stops.» — بدون مرجع
```
The same alien corridor now calm again: red lights turned off, soft teal light back, blast doors open, empty and silent. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**57** · «Daniel reconnects a loose cable and activates the backup release.» — مرجع: `DANIEL`
```
Close-up of the stickman Daniel's hands from the reference connecting two thick cable ends inside an open wall panel, a bright spark jumping between them, his face lit by the spark. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**58** · «A heavy door begins to open. The sound echoes… You freeze.» — مرجع: `RAY` + `JAX` + `DANIEL`
```
A massive heavy metal door slowly sliding open with dust falling from its edges; in front of it the three stickmen from the references freeze mid-step, wincing at the loud noise. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**59** · «Somewhere nearby, an alien responds to the noise.» — مرجع: `ALIEN`
```
In a dim side corridor, a tall green alien from the reference stops and sharply turns its head toward the camera, eyes starting to glow, listening. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**60** · «But your last bottle of water is empty.» — مرجع: `RAY`
```
Close-up of the grey-cap stickman's hand from the reference shaking an empty clear water bottle upside down, not a single drop falling, his worried face blurred behind it. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۹ — DAY 20

**61** · «You finally reach the hangar… one alien guard is standing near the entrance.» — مرجع: `ALIEN` + `RAY` + `JAX` + `DANIEL`
```
Wide shot of the vast alien hangar: the small silver shuttle in the center; one tall green alien from the reference stands guard near its entrance ramp; in the foreground the three stickmen hide behind a huge support column, peeking around it. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**62** · «…you use the identification card on the shuttle's access panel. The door opens.» — مرجع: `RAY`
```
The grey-cap stickman from the reference presses the glowing card to the shuttle's access panel; the shuttle's side door hisses open with a burst of white light and steam. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**63** · «Under the seats, you find an emergency kit… Jax drinks first.» — مرجع: `JAX` + `SHUTTLE`
```
Inside the shuttle cockpit from the reference: an emergency hatch under the seats is open, revealing water bottles and wrapped food blocks; the black-beanie stickman from the reference drinks greedily from a bottle, eyes closed in relief. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**64** · «Daniel moves toward the control panel… The display lights up.» — مرجع: `DANIEL` + `SHUTTLE`
```
The stickman Daniel from the reference sits in the pilot seat of the shuttle cockpit, hands hovering over the glowing console, three large screens lighting up with blank bright teal glow, the stars visible through the window. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**65** · «You select Earth as the destination.» — مرجع: `SHUTTLE`
```
Close-up of a shuttle navigation screen showing a simple glowing map of the solar system with a small bright blue planet highlighted by a glowing circle, a finger touching it. No letters or numbers on the screen. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**66** · «Then the display changes. You stare at the screen.» — مرجع: `SHUTTLE`
```
The same navigation screen now glowing red, the highlight circle jumped from the blue planet to a small red planet; red light spilling onto the cockpit. No letters or numbers on the screen. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**67** · «Jax turns toward you. “What?”» — مرجع: `RAY` + `JAX` + `DANIEL` + `SHUTTLE`
```
Inside the shuttle cockpit, the three stickmen from the references stare at the red-glowing screen in disbelief; the black-beanie stickman turns his head toward the grey-cap stickman with a shocked open mouth. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**68** · «The hangar doors start closing. An alien appears outside the shuttle.» — مرجع: `ALIEN`
```
View from inside the shuttle cockpit through the front window: the giant hangar doors closing in the background, red alarm lights flashing, and a tall green alien from the reference standing right outside the window, staring in, eyes glowing with scanning light. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**69** · «The shuttle launches just before the doors close.» — بدون مرجع
```
Exterior shot: a small silver shuttle blasting out through the narrowing gap of two huge closing hangar doors of a colossal alien mothership, engine flames bright teal, sparks and debris, stars behind. Dynamic and explosive. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**70** · «For the first time in twenty days, you're free. But you're not going home.» — بدون مرجع
```
Wide space shot: the tiny silver shuttle flying away into the dark, the giant alien mothership shrinking behind it, a distant small red dot of Mars ahead. Quiet, lonely, bittersweet. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۱۰ — DAY 22

**71** · «A human spacecraft needs about seven months to reach Mars.» — بدون مرجع
```
Simple infographic-style space illustration: Earth on the left, Mars on the right, a long dotted curved path between them with a small classic human spacecraft on it, a starry dark background. No text, no numbers. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**72** · «You shut down every system you don't need… The cabin turns cold.» — مرجع: `SHUTTLE`
```
The shuttle cockpit from the reference with all screens and lights switched off, only a faint blue starlight through the window, thin frost forming on the metal surfaces and window edges, visible cold. Silent and dark. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**73** · «You put the suits back on.» — مرجع: `SUITS` + `DANIEL` + `SHUTTLE`
```
In the cold dark shuttle cockpit, the three stickmen sit strapped in their seats wearing the white protective suits with clear bubble helmets from the reference (Daniel in a matching suit, orange jumpsuit visible underneath), small teal lights glowing on their wrists. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**74** · «And then you do the hardest thing. Nothing. You stay still. You breathe slowly.» — مرجع: `RAY` + `SUITS`
```
Close-up of the grey-cap stickman's face inside a clear bubble helmet from the reference, eyes half closed, breathing slowly and calmly, a faint fog of breath on the inside of the visor, stars reflected on the glass. Calm, meditative, fragile. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۱۱ — DAY 27

**75** · «A large red planet fills the window. Mars.» — مرجع: `SHUTTLE`
```
View from inside the shuttle cockpit through the front window: the huge red planet Mars fills the entire window, craters and dusty red surface details, thin pale atmosphere glow at its edge, the silhouettes of three helmeted heads in the foreground. Awe and dread. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**76** · «The air on Mars is about one percent as thick as Earth's.» — بدون مرجع
```
Simple comparison illustration: on the left, Earth with a thick glowing blue atmosphere layer; on the right, Mars with an extremely thin, barely visible pale atmosphere layer; dark space background. No text, no numbers. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**77** · «The heat shield glows as the outside temperature rises.» — بدون مرجع
```
Exterior shot of the small silver shuttle plunging into the Martian atmosphere at an angle, its bottom heat shield glowing bright orange and white, a trail of fiery plasma behind it, the red planet below. Dramatic. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**78** · «He breaks it in half and gives you one. “Later is now.”» — مرجع: `RAY` + `JAX` + `SUITS`
```
Inside the shaking shuttle cockpit with orange glow coming through the window, the black-beanie stickman in a white protective suit with his helmet visor open hands half of a small chocolate piece to the grey-cap stickman, a brave tired smile on his face. Emotional, warm moment amid chaos. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۱۲ — DAY 29

**79** · «CONTROL SYSTEM FAILURE. The shuttle begins spinning.» — مرجع: `DANIEL` + `SHUTTLE`
```
Chaotic shuttle cockpit bathed in flashing red warning light, sparks bursting from the console, the horizon of Mars tilting sharply through the window; the stickman Daniel in a suit from the reference fights the controls, the others pressed into their seats. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**80** · «The surface of Mars is rushing toward you.» — بدون مرجع
```
Exterior shot: the small silver shuttle spinning out of control toward the red rocky surface of Mars, trailing smoke, red canyons and rocks below, dusty orange sky. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**81** · «The shuttle hits the ground. Metal tears apart.» — بدون مرجع
```
Exterior impact shot: the shuttle crashing into red Martian sand, a huge explosion of red dust and rocks, metal pieces flying, a long trench carved behind it. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

---

## فصل ۱۳ — DAY 30

**82** · «You slowly open your eyes… Smoke fills the cabin.» — مرجع: `RAY` + `SUITS`
```
Close-up inside a cracked clear bubble helmet: the grey-cap stickman from the reference slowly opening his eyes, dazed, thin smoke drifting through the broken dark cabin behind him, a faint red light. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**83** · «You look toward Jax. He's still breathing. …Daniel coughing.» — مرجع: `JAX` + `DANIEL` + `SUITS`
```
Inside the wrecked shuttle cabin full of thin smoke: the black-beanie stickman in a white suit slumped in his seat but breathing, fog on his visor; behind him the stickman Daniel coughing, pushing debris off his lap. Dusty red light through cracks. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**84** · «Red sand. Rocks. A dark sky.» — بدون مرجع
```
View through a broken shuttle window with cracked glass edges: an endless Martian landscape of red sand dunes and scattered dark rocks, a dark dusky sky with a small pale sun, silent and empty. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

**85** · «You're on Mars… And now, you have thirty days to survive.» — مرجع: `RAY` + `JAX` + `DANIEL` + `SUITS`
```
Epic wide final shot: the crashed silver shuttle half buried in red Martian sand, a long trench behind it, three tiny stickmen in white protective suits standing beside the wreck looking out over the vast red desert under a dark sky. Lonely, epic, cliffhanger. Detailed hand-drawn 2D cartoon illustration, thick clean black outlines, smooth cel shading with soft gradients, cinematic lighting, rich detailed background, sharp focus, 16:9, no text, no letters, no watermark.
```

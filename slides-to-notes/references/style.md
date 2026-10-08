# Oliver's note style

Handwritten on an iPad, one accent color per course (EECS 280 = blue/purple, CS HL = green with
purple highlighter, Japanese = red). Black for normal text, accent for anything important.

## How the page looks

- **Page header:** `LECTURE 4 – MACHINE MODEL PART I` in caps (number in accent, topic in black).
- **Section headings:** short, ALL CAPS, highlighted: `VARIABLES & MEMORY`, `SCOPE`, `C++ TYPES`.
- **Definitions:** one plain sentence, then sub-points with a hooked arrow `↳`.
- **Key terms** are written in the accent color inside the sentence, not defined separately.
  In markdown, show accent color as **bold**.
- **Code:** short snippets (2–5 lines) with arrows/labels pointing at the parts
  (`int x = 10+5;` with `type`, `name`, `declaration` under it), `// 0x1000` comments for results,
  and `}` braces grouping lines with a label (`} declaration`, `} assignments`).
- **Transformations:** `3 → 3.0  widening`, `2.7 → 3  truncating`.
- **Decision trees** for "which should I use" rules: `modify the obj? —yes→ void f(Person &p);`, `↓ no`.
- **Two columns** when ideas pair up (explanation left, code right), and a **`MISC DETAILS`**
  sidebar on the left for small facts that don't need a section.
- **Lists:** numbered `1. 2. 3.` for enumerations; `1) 2)` for examples; `a) b)` for sub-cases.
- **Tone: full sentences.** Every section opens with 1–3 complete sentences that define the idea
  properly ("A scope is a region of the source code where names are meaningful. Often they are
  defined with {} to create blocks. A variable may be used only if it's in scope."). The `↳` points
  are full sentences too. Casual wording is fine ("we wanna", "e.g.", "e.t.c", "&"), but don't cut
  sentences down to fragments: a first draft written in fragments was too terse for Oliver to follow.

## How the handwriting maps to the page template

| Handwriting | In `assets/notes-template.html` |
|---|---|
| highlighted heading | `<h2>` inside a `.sec` |
| accent-color term | `<span class="term">` |
| hooked sub-point | `<li>` in `ul.arrows` |
| arrows / labels on code | a `.ln` row: `<code>` plus `<span class="note">` |
| brace grouping | one `.note` on the last grouped row (`} assignments`) |
| sidebar | the `aside.misc` list |
| two columns | a `.pair` grid, only when the pairing matters |

The examples below are plain-text transcriptions of his pages, so they use `**bold**` for accent
color and `###` for highlighted headings. Those marks stand for styling; don't put them on the page.

## Example 1: EECS 280, Lecture 4 (programming, concept + code)

```
LECTURE 4 – MACHINE MODEL PART I

### VARIABLES & MEMORY                 ### DEFAULT INITIALIZATION
A variable is a name that refers to     Objects can be explicitly initialized, or it is
an object in memory. Data is stored     default-initialized.
in bytes composed of 8 bits. **Type**   ↳ For **atomic types** like int, bool e.t.c, this is
tells you how much space it needs.        undefined. This is called **memory junk**
                                        ↳ For **class types**, a default constructor
                                          ensures a value exists

### ASSIGNMENT & VALUE SEMANTICS
C++ has **value semantics**: variables always refer to the same object once declared.
An **assignment** copies a value from one object to another.

Every object lives at some **address**        int x = 10+5;
in memory. The **&-operator** yields the      int y = 0;      // } declaration
address of an object                          cout << &x;     // 0x1000
                                              cout << &y;     // 0x1004
A **reference** declaration binds a           y = x;
variable to an existing object, giving        x = 20;         // } assignments
it multiple **aliases**                       cout << &x;     // still same

int& = reference to int
int x = 10+5;
int& r = x;
cout << &x   // 0x1000
cout << &r   // 0x1000
```

## Example 2: CS HL, networking (definition-heavy, no code)

```
### INTERNET
↳ A global **WAN** with millions of computers & networks
↳ Provides all services like WWW or file transfer
↳ Internet is decentralized so no central storage of data
    ↳ Anyone can share services
↳ Access to internet via providers (ISP) }— broadband via cable modem/DSL
                                            — Wi-Fi via routers
                                            — Mobile network e.g 3G/4G

### VPN or **virtual private networks**
↳ A computer network that connects computer systems but also allows remote clients
  appear physically present in the **LAN**
↳ Works by making a tunnel through public networks to access the private network
↳ **VPN Types**:
    ↳ Site-to-site: connects entire networks & gives secure data interchange
    ↳ Remote: connects individual hosts to private networks via internet
```

## Example 3: Japanese, Tobira Lesson 1 (grammar point + examples)

```
### 3. の Noun modifying particle
Using **の**, you can modify a noun with another noun. In N1 の N2, N1 provides
information to describe or specify N2.
  a) Possession – N2 is possessed by N1
     わたしのほん                **my books**
  b) Affiliation – N2 is affiliated with N1
     にほんのうた                **songs from Japan**
```

Note how every example is the *smallest* one that shows the rule, and translations/results sit
to the right in the accent color.

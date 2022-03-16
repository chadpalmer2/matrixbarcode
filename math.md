# Algebraic Coding Theory - Mary Wootters

## Lecture 1

### Video 1: Motivation, the basic problem

Setup: 
- We have a message $x$ of length $k$.
- We have an encoding scheme which takes $x$ and produces codeword $c$ of length $n > k$. 
- This codeword is corrupted to $\tilde{c}$ through a noisy channel.
- We have a decoding scheme which take $\tilde{c}$ and produces $x$.

Basic problem of coding theory: 
- Determine an encoding and decoding scheme which is good, by some metric.

Examples:
- Alice wishes to communicate $x \in \{0, 1\}^k$ to Bob, but a noisy channel converts $x$ into $\tilde{x} \in \{0, 1\}^k$
- We wish to store on a server $x \in \{0, 1\}^k$, but environmental damage converts $x$ into $\tilde{x} \in \{0, 1\}^k$
- More across computer science and mathematics

Metrics of "Good":
- Handle bad actions on our data
- Recovering information regarding $x$
- Minimizing overhead: $\frac{k}{n}$
- Doing so efficiently

Difficulty:
- Trade-offs between various concerns
- Defining concerns in concrete ways

### Video 2: Definitions and examples

Code Definition
- a **code** $C$ of **block length** $n$ over an **alphabet** $\Sigma$ is $C \subseteq \Sigma^n$. The elements $c \in C$ are **codewords**.
- Example: $C = \{HELLOWORLD, BRUNCHTIME, CHADPALMER\}$ is a code of block length 10 over $\Sigma = \{A, B, ..., Z\}$
- Example: $C = \{(0,0,0,0), (1,0,1,0)\}$ is a code of block length 4 over $\Sigma = \{0, 1\}$ (a binary code!)

Relationship to Alice and Bob: Example 1
- Consider **encoding map** from $\{0, 1\}^3 \rightarrow \{0, 1\}^4$:
$$ENC(x_1, x_2, x_3) = ENC(x_1, x_2, x_3, x_1 + x_2 + x_3 \mod 2)$$
- Note that the *code* is the image of the encoding map
- This code can **correct** one **erasure** (we know which bit was erased): given an erased bit, we can determine what it should have been (what adds to $0 \mod 2$?)
- This code can **detect** one **error** (we don't know what bit was changed), cannot however fix that error

Correcting an error: Example 2
- Consider $ENC(x_1, x_2, x_3, x_4) = (x_1, x_2, x_3, x_4, x_2 + x_3 + x_4 \mod 2, x_1 + x_3 + x_4 \mod 2, x_1 + x_2 + x_4 \mod 2)$ (this is the Hamming code!)
- This code can correct an error: checking all three parity bits locates exact bit where error occurred

More definitions
- The **Hamming distance** between $x, y \in \Sigma^n$ is a metric defined as
$$ \Delta(x, y) = \sum_{i=1}^n 1\{x_i \neq y_i\} $$
- The **relative hamming distance** between $x, y \in \Sigma^n$ is
$$ \delta(x, y) = \frac{\Delta(x, y)}{n} $$
- The **minimum distance** of a code $C \subseteq \Sigma^n$ is
$$ \min_{c \neq c' \in C} \Delta(c, c') $$

Minimum Distance is a proxy for robustness
- Theorem: A code with minimum distance $d$ can:
    - Correct $\leq d-1$ erasures
    - Detect $\leq d-1$ errors
    - Correct $\leq \lfloor\frac{d-1}{2}\rfloor$ errors
- Proof
    - Consider arbitrary $c$, $c'$ closest codeword to $c$. We may consider Hamming balls of radius $d-1$ and $\lfloor\frac{d-1}{2}\rfloor$ around both $c$ and $c'$
    - For (1) and (3), algorithm for $\tilde{c}$ is as follows: return $c \in C$ such that $\Delta(c, \tilde{c})$ is minimized.
    - For (2): if $\tilde{c} \in C$, return "NO ERROR", else return "ERROR"
    - Correctness of (3): $\tilde{c}$ must be in ball of radius $\lfloor\frac{d-1}{2}\rfloor$ around $c$, not in same ball around $\tilde{c}$. Thus $c$ is returned.
    - Correctness of (2): $\tilde{c}$ must be in ball $d-1$ around $c$, then $\tilde{c} \not\in C$.
    - Correctness of (1): Impossible for $d$ differences in $c, c'$ to be in $d - 1$ spots where erasures occurred. Then there can be only one codeword in $C$ with unerased values equal to that of $\tilde{c}$
- Examples:
    Example 2 had distance 2
    Example 3 had distance 3

Definitions
- The **message length** or **dimension** of a code $C$ over an alphabet $\Sigma$ is defined to be $k = \log_{|\Sigma|}|C|$ (same as length from before)
- The **rate** of a code $C \subseteq \Sigma^n$ is
$$ R = \frac{\log_{|\Sigma|}|C|}{n} = \frac{\text{message length}}{\text{block length}} $$
- $R \in [0, 1]$. $R$ close to 1 is desirable.
- Code with distance $d$, message length $k$, and block length $n$ over an alphabet $\Sigma$ is called an $(n, k, d)_{|\Sigma|}$ code

Returning to "concerns"
- (1) and (2) can be concatenated into the concern that "We want minimum distance d" (AKA we want corrective power stated above)
    - Note that these are worst case errors
- (3) can be expressed as "We want rate as close to 1 as possible"
- Thus, (setting aside issues of algorithmic efficiency), we wish to know the best trade-off between rate and distance.
    - This is an open problem for binary codes.

### Video 3: The Hamming bound

Question: What is the best trade-off between rate and distance?

Motivation
- Consider $|C|$ codewords in $\Sigma^n$ with disjoint Hamming balls of radius $\lfloor\frac{d-1}{2}\rfloor$
- There must be a bound on the number of balls, or they will not fit in $\Sigma^n$

Volume of Hamming Balls
- A **Hamming ball** in $\Sigma^n$ of radius $e$ about $x \in \Sigma^n$ is
$$ B_{\Sigma^n} (x, e) = \{ y \in \Sigma^n : \Delta(x, y) \leq e \} $$
- The volume of $ B_{\Sigma^n} (x, e) $ is
$$ \text{Vol}{|\Sigma|} (e, n) = |B_{\Sigma^n} (x, e)| $$
- Note that balls are the same volume around any $x$ by symmetry, so $x$ is not on left side of equation

Explicit formula
$$ \text{Vol}_q(e, n) = \sum_{i = 0}^e \binom{n}{i} (q - 1)^i $$

Quick definition of weight (helpful for proving volume formula):
- wt $(x) = $ # of nonzero entries of $x$

Returning to previous intuition to derive Hamming bound
- Let $C \subseteq \Sigma^n$ be code with distance $d$ and message length $k$. Let $q = |\Sigma|$. Then $|C|\text{Vol}_q(\lfloor\frac{d-1}{2}\rfloor, n) \leq q^n $
- This is interpreted as "total volume of disjoint Hamming balls" is less than or equal to "total volume of $\Sigma^n$
- Taking log base $q$ of both sides, dividing through by $n$, and rearranging yields the Hamming bound:
$$ R = \frac{\log_{q}|C|}{n} \leq 1 - \frac{\log_q(\text{Vol}_q(\lfloor\frac{d-1}{2}\rfloor, n))}{n} $$

An example
- Example three had $k = 4, n = 7, d = 3, q = 2$
- Plugging into Hamming bound, we see $R = \frac{k}{n} \leq \frac{4}{7}$
- Hamming code actually achieves this bound - thus, for binary alphabet, 3 bits is the smallest overhead you can add to words of length 4 to achieve distance 3

## Lecture 2

### Video 1: Hamming code revisited

Recall the Hamming code of length 7.
- We will consider a number of different, more generalizable interpretations.

Linear algebra:
    - $G$ is a **generator matrix**
    $$ G = \begin{pmatrix}
    1&0&0&0\\
    0&1&0&0\\
    0&0&1&0\\
    0&0&0&1\\
    0&1&1&1\\
    1&0&1&1\\
    1&1&0&1\\
    \end{pmatrix} $$
    $$ ENC(\overline{x}) = G\overline{x} \mod 2 $$

- Observations
    - $C$ is closed under addition
        - For any $c, c' \in C$, $c + c' = Gx + Gx' = G(x + x') \in C$
    - $C$ is a **linear subspace** of $\{0, 1\}^7$ of dimension 4
        - $C = \text{column-span}(G)$
    - The distance of $C$ is the same as the **minimum weight** of any nonzero $c \in C$
        - $\Delta(c, c') = \Delta(Gx, Gx') = \Delta(Gx - Gx', 0) = \text{wt}(G(x - x'))$
        - Thus, for any distance between code words, there is another code word with that distance as its weight

- Another interpretation: $H$ is a parity check matrix
    $$ H = \begin{pmatrix}
    0&1&1&1&1&0&0\\
    1&0&1&1&0&1&0\\
    1&1&0&1&0&0&1\\
    \end{pmatrix} $$
    $$ H \begin{pmatrix}
    x_1\\
    x_2\\
    x_3\\
    x_4\\
    c_5\\
    c_6\\
    c_7\\
    \end{pmatrix} = 
    \begin{pmatrix}
    0\\
    0\\
    0\\
    \end{pmatrix}
    $$
    - $\forall c \in C, Hc = 0$

- Observations
    - $C \subseteq \ker(H)$
        - $\dim(\ker(H)) = 7 - \text{rank}(H) = 7 - 3 = 4$
        - $\dim(C) = 4$
        - Thus, $C = \ker(H)$
    - $C$ has distance 3 - Proof
        - If suffices to show that the minimum weight of $C$ is 3
        - Suppose $c \in C$ has weight 1 or 2
        - Recall $Hc = \overline{0}$. This would imply, however, that there is a nontrivial combination of $\leq 2$ columns of $H$ that sums to $\overline{0}$
        - However, any pair of columns of $H$ are linearly independent
        By contradiction, $\text{wt}(c) \geq 3, \forall c \in C$. Then $\text{Distance}(C) \geq 3$
        - Consider that $(0, 1, 0, 1, 0, 1) \in C$ has weight 3, so $\text{Distance}(C) \leq 3$.
        - Thus, $C$ has distance 3

- Efficient decoding algorithm
    - Compute $H\tilde{c}$. This will be a column of $H$, corresponding to the flipped bit.
    - Proof: Let $z$ be error vector of weight 1, so $\tilde{c} = c + z$. Then $H\tilde{c} = H(c + z) = Hc + Hz = Hz$. $z$ has weight 1, so $Hz$ must equal a column of $H$ corresponding to the entry at which $z_i = 1$. This is the flipped bit in $\tilde{c}$.

- Caution: all of this assumes linear algebra works well $\mod 2$. This is a generous assumption to make that we have yet to show is true.

### Video 2: A cautionary tale

- Attempting to do the Hamming code over $\mod 4$ fell apart quickly

### Video 3: Finite fields

A **field** $\mathbb{F}$ is a set of elements, along with operations + and *, such that associativity, commmutativity, and distributivity hold, and identities and inverses exist 
- Integers $\mod 5$ are a finite field
- Integers $\mod 4$ are not
    - This is why the example in Video 2 fell apart
- A **finite field** is a field over a finite set

Theorem:

- For every prime power $p^t$, there is a unique finite field with $p^t$ elements called $\mathbb{F}_{p^t}$ or $GF(p^t)$
- No other finite fields exist
- Note $\mathbb{F}_p = \{0, 1, ..., p - 1\} \mod p$
- See abstract algebra for proof

Linear algebra generally works over finite fields
- Let $\mathbb{F}$ be a finite field
- $\mathbb{F}^n = \{(x_1, ..., x_n): x_i \in \mathbb{F} \}$
- A **subspace** $V$ \subseteq \mathbb{F}^n$ is a set that is closed under addition and scalar multiplication
- $v_1, ..., v_t \in \mathbb{F}^n$ are **linearly independent** if $\forall \lambda_1, ..., \lambda_n \in \mathbb{F}$ not all 0, $\sum_i \lambda_iv_i \neq 0$
- the span of $V' = v_1, ..., v_t \in V$ is equal to the set of a linear combinations of vectors in $V'$
- a **basis** for a subspace $V \subseteq \mathbb{F}^n$ is  a set $V' = v_1, ..., v_t \in V$ such that $V'$ are linearly independent and $\text{span}(V') = V$
- **dimension** of subspace $V$ is the number of elements in any basis of $V$

Considerations
- Most geometric intuitions like angles don't hold in finite field linear algebra
- Error-correcting codes are done using finite fields, as linear algebra is defined primarily over finite fields (see modules for exceptions)

### Video 4: Linear codes




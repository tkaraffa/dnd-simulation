The probability of hitting with an attack roll follows a roughly Bernoulli distribution, where

```
P(Hit) = 1 - (Target AC - Hit Modifiers - 1) / 20 if x = 2, 3, ..., 19
        1 if x = 20
        0 if x = 1
```

```

The difference is that there is always a 5% chance of a miss (rolling a 1), and there is always a 5% chance of a hit (rolling a 20), regardless of whether the roll would have hit or missed due to AC or modifiers.

Therefore, hitting a target always has, at minimum, a probability of 0.05, and, at most, a probability of 0.95. For the other 90% of possible values, the above formula determines the probability of a hit given a target's AC and the character's hit modifiers.

The following shows the probability of hitting given a target's AC, and assuming a hit modifier of 0:

```
AC P
1 0.95
2 0.95
3 0.9
4 0.85
5 0.8
6 0.75
7 0.7
8 0.65
9 0.6
10 0.55
11 0.5
12 0.45
13 0.4
14 0.35
15 0.3
16 0.25
17 0.2
18 0.15
19 0.1
20 0.05
21 0.05
```

For every point of hit modifier, the probabilities of this table can be shifted one row down (for positive change) or up (for negative change). This can be shown with the same calculations, but with a modifier of +1:

```
AC P
1 0.95
2 0.95
3 0.95
4 0.9
5 0.85
6 0.8
7 0.75
8 0.7
9 0.65
10 0.6
11 0.55
12 0.5
13 0.45
14 0.4
15 0.35
16 0.3
17 0.25
18 0.2
19 0.15
20 0.1
21 0.05
```

As AC increases in value, the percentage of rolls that would hit decreases at an increasing rate. Assuming a to-hit bonus of 0, a change from 5 AC to 7 AC results in a relative decrease in the probability of being hit of 11.8%, but a change from 15 AC to 17 AC results in a relative decrease of 40%. What this means is that the higher an AC is, the more it will benefit from further increases. However, the benefits of an ever-increasing AC are capped when the target's AC equals or exceeds the to-hit bonus of an attacker by 20; at that point, and at any higher AC, only a 20 will cause a hit.





grand sample mean is sample mean of sample means!
sample variance: S^2 = 1/(r-1) * sum(Z i - Z bar r )^2
SPYRE - Simple Python 3 RegExp Engine
====================================

Weekend project, it can compile and match against common RegExps.
Does not support backtracking so do not feed sick RegExps to it.
It can handle successfully stuff like:

 * _"abcd[0-9]+[a-z]*"_
 * _"[a-z]*[1-9][1-9]8[1-9]"_
 * _"[0-9]+[^a-z]*"_

Subset of RegExp syntax supported
---------------------------------
* _"^"_ Matches the starting position within the string. In line-based tools, it matches the starting position of any line.

* _"."_ Matches any single character (many applications exclude newlines, and exactly which characters are considered newlines is flavor-, character-encoding-, and platform-specific, but it is safe to assume that the line feed character is included). Within POSIX bracket expressions, the dot character matches a literal dot. For example, a.c matches "abc", etc., but [a.c] matches only "a", ".", or "c".

* _"\*"_ Matches the preceding element zero or more times. 
For example, ab\*c matches "ac", "abc", "abbbc", etc. [xyz]* 
matches "", "x", "y", "z", "zx", "zyx", "xyzzy", and so on. (ab)* matches "", "ab", "abab", "ababab", and so on.

* _"?"_	Matches the preceding element zero or one time. For example, ab?c matches only "ac" or "abc".

* _"+"_ Matches the preceding element one or more times. For example, ab+c matches "abc", "abbc", "abbbc", and so on, but not "ac".

* _"[ ]"_ A bracket expression. Matches a single character that is contained within the brackets. For example, [abc] matches "a", "b", or "c". [a-z] specifies a range which matches any lowercase letter from "a" to "z". These forms can be mixed: [abcx-z] matches "a", "b", "c", "x", "y", or "z", as does [a-cx-z].
The - character is treated as a literal character if it is the last or the first (after the ^, if present) character within the brackets: [abc-], [-abc]. Note that backslash escapes are not allowed. The ] character can be included in a bracket expression if it is the first (after the ^) character: []abc].

* _"[^ ]"_ Matches a single character that is not contained within the brackets. For example, [^abc] matches any character other than "a", "b", or "c". [^a-z] matches any single character that is not a lowercase letter from "a" to "z". Likewise, literal characters and ranges can be mixed.

* _"$"_ Matches the ending position of the string or the position just before a string-ending newline. In line-based tools, it matches the ending position of any line.

Limitations
-----------
* Square brackets can contain only a sequence or a range, not both
* No backtracking
* Matches only the first occurrence
# Unit Conversion Bot

u/unit-convert was created by u/jac0b_0 moderator of r/deletedredditor

This bot will **only work when mentioned** to stop it becoming a spam machine. It will **usually take less than 15 minutes to reply although could take longer.**

Any problems, bugs or ideas post them in the subreddit (u/unit_convert)

---

## Links

- [See list of units](https://www.reddit.com/r/unit_convert/wiki/units)
- [See list of prefixes](https://www.reddit.com/r/unit_convert/wiki/prefixes)

---

## Syntax

- Syntax: `u/unit-convert <magnitude> <unit> to|in <unit>`
  - **Units and prefixes are case-sensitive**
  - Units never have a space use an underscore instead e.g `cubic_centimeter`
- Do a simple conversion between two units (**case-sensitive**): `u/unit-convert 1000 meters to yards` or 
  - [See list of units](https://www.reddit.com/r/unit_convert/wiki/units)
- Full unit name isn't needed `u/unit-convert 1000 m in yd`
- You can also use prefixes (**case-sensitive**): `u/unit-convert 1000 kilometers to micrometers`
  - [See list of prefixes](https://www.reddit.com/r/unit_convert/wiki/prefixes)
- You can use E notation in your values: `u/unit-convert 1e3 km in um`
- You can also convert to multiple units: `u/unit-convert 1000 km to um yards lightyears`
  - Outputs 1000km in micrometers, yards and lightyears
- You can also do currency conversions: `u/unit-convert 100 USD to GBP`
  - You **must use currency codes** `u/unit-convert $100 to GBP` will **not** work
  - List of available codes are listed in the [list of units](https://www.reddit.com/r/unit_convert/wiki/units)
- You can also convert between temperatures: `u/unit-convert 20 degF in degC`
- You can use derived units using this syntax
  - Speed: `u/unit-convert 20m/s to mph`
  - Acceleration: `u/unit-convert 20m/s^2 in mph/hr` or `u/unit-convert 20m(s^-2) to mph/hr`
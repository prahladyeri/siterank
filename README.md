![pypi](https://img.shields.io/pypi/v/siterank.svg)
![python](https://img.shields.io/pypi/pyversions/siterank.svg)
![license](https://img.shields.io/github/license/prahladyeri/siterank.svg)
![docs](https://readthedocs.org/projects/siterank/badge/?version=latest)
[![patreon](https://img.shields.io/badge/Patreon-brown.svg?logo=patreon)](https://www.patreon.com/prahladyeri)
[![paypal](https://img.shields.io/badge/PayPal-blue.svg?logo=paypal)](https://paypal.me/prahladyeri)
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://twitter.com/prahladyeri)

# siterank
A python script to get alexa global rank for a given website or domain.

**Note:**

As of February 2023, Amazon's Alexa API has been retired. Consequently, I've switched to [SimilarWeb API](https://www.similarweb.com/corp/ranking-api/)'s free-tier for fetching these rankings. When you run the  program for the first time, it'll prompt you to create a SimilarWeb account and store the API key to the settings JSON file.

# Installation

	pip install siterank

# Usage

```bash
C:\> siterank google.com twitter.com linkedin.com upwork.com
successfully imported cache db..
found in cache: google.com
found in cache: twitter.com
fetching live: linkedin.com
found in cache: upwork.com
4/4. upwork.com

********************************************************************************
  Website                                 Rank
********************************************************************************
  google.com                              1
  twitter.com                             5
  linkedin.com                            17
  upwork.com                              730
```
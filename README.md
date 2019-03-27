<a href="https://www.amazon.it/sfal-Idiomi-Inglesi/dp/B07PY85HXR/ref=sr_1_fkmrnull_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=idiomi+inglesi&qid=1553682169&s=alexa-skills&sr=1-1-fkmrnull"><img src="https://i.imgur.com/rdBp0SM.png" title="IdiomiInglesi" alt="IdiomiInglesi"></a>

# Alexa Skill: Idiomi Inglesi (English Idioms)

> Alexa Skill written in Python that teaches you English idioms in Italian.

> More than 100 idioms read by the English voice of Alexa. Explanations and examples are provided in Italian.

## Example

```def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In IdiomaHandler")

        random_fact = random.choice(idioms_data.data)
        idiom = random_fact["Idioma"]
        meaning = random_fact["Significato"]
        example = random_fact["Esempio"]

        speech = GET_FACT_MESSAGE + ("<voice name='Emma'><lang xml:lang='en-GB'>{}</lang></voice>. Significa: {}. Ecco un esempio: <voice name='Emma'><lang xml:lang='en-GB'>{}</lang></voice>".format(idiom, meaning, example))
```

---

## Enable Skill (Italy only)


- <a href="https://www.amazon.it/sfal-Idiomi-Inglesi/dp/B07PY85HXR/ref=sr_1_fkmrnull_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=idiomi+inglesi&qid=1553682169&s=alexa-skills&sr=1-1-fkmrnull" target="_blank">Idiomi Inglesi on Amazon.it</a>


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- [MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2019 © <a href="https://github.com/sfal" target="_blank">sfal</a>.

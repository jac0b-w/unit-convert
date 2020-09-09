#!/usr/bin/python3.7

print("Content-Type: text/html\n\n")

print("-------------RESTART-------------")
import praw
import re
import pint
import requests
import configparser
# import time
# from itertools import count


class Const:
    bot_name = "u/unit-convert"
    about_link = "https://www.reddit.com/r/unit_convert/wiki/about"
    units_link = "https://www.reddit.com/r/unit_convert/wiki/units"
    prefixes_unit = "https://www.reddit.com/r/unit_convert/wiki/prefixes"


class ParseComment:
    def __init__(self, comment_text):
        regex_float = "(-?\d)([^A-Z\s]|\^)*(e([^A-z\s]|\^)+)?"
        # No operators: -?\d+(.\d+)?(e-?\d+)?
        # Can do math: (-?\d)([^A-Z\s]|\^)*(e([^A-z\s]|\^)+)?
        regex_unit = "[^\d\s]\S*"
        try:
            self.command = re.search(
                f"{Const.bot_name} +{regex_float} *{regex_unit} +(to|in) +{regex_unit}( +{regex_unit})*",
                comment_text,
                re.IGNORECASE
            ).group(0)
        except AttributeError:
            raise InvalidSyntaxError
        self.command = re.sub(' +', ' ', self.command)
        self.from_ = re.search(f"{regex_float} *{regex_unit}", self.command, re.IGNORECASE).group(0)
        if " to " in self.command:
            s = "to"
        elif " in " in self.command:
            s = "in"
        self.to_units = re.search(
            f"{s} +{regex_unit}( +{regex_unit})*",
            self.command,
            re.IGNORECASE).group(0).lstrip(f"{s} ").split(" ")

    def __str__(self):
        return f"command:{self.command}\nfrom:{self.from_}\nto:{self.to_units}"


class InvalidSyntaxError(Exception):
    pass


class Reply:
    def __init__(self, comment, ureg, debug=False, debug_body=None):
        self.debug = debug
        self.comment = comment
        try:
            parsed_command = ParseComment(self.comment.body)
            if debug:
                if debug_body is not None:
                    parsed_command = ParseComment(debug_body)
                print(parsed_command)
        except InvalidSyntaxError:
            self.reply(
                self.final_text("Sorry I don't understand this. "\
                f"Try using the form `{Const.bot_name} <magnitude><unit> in|to <unit>`")
            )
            return
        
        try:
            init_q = ureg(parsed_command.from_)
        except pint.UndefinedUnitError as e:
            self.reply(self.final_text(self.format_errors(e)))
            return
        
        final_qs = []
        errors = []
        for unit in parsed_command.to_units:
            try:
                final_qs.append(init_q.to(unit))
            except (pint.DimensionalityError, pint.UndefinedUnitError) as e:
                errors.append(e)

        final_reply = self.final_text(
            self.format_body(init_q, final_qs),
            self.format_errors(*errors)
        )

        self.reply(final_reply)

    def reply(self, reply_msg):
        if self.debug:
            print(reply_msg)
            return

        try:
            self.comment.reply(reply_msg)
            print(f"replied to {self.comment.author}")
            self.comment.mark_read()
        except praw.exceptions.RedditAPIException: # RedditAPIException: # rate limit
            print(f"Failed to reply to {self.comment.author}")

    @staticmethod
    def final_text(*strings):
        # add footer
        strings = list(s for s in strings if s != "")
        strings.append(
            f"###### *I am a bot* [Find out more]({Const.about_link})")
        return "\n\n---\n\n".join(strings)

    @staticmethod
    def format_unit(unit):
        return str(unit)\
            .replace('_',' ').replace(' / ','/').replace(' ** ','^')

    @staticmethod
    def format_dim(dim):
        return str(dim).replace(' / ','/').replace(' ** ','^')

    @classmethod
    def format_quantity(cls,q):
        output = "{:-1.7g}".format(q.magnitude).replace("+","")
        output += f" {cls.format_unit(q.units)}"
        return output

    @classmethod
    def format_body(cls, init_q, final_qs):
        output = f"{cls.format_quantity(init_q)} is"

        if len(final_qs) == 0:
            return ""

        if len(final_qs) == 1:
            return output + f" {cls.format_quantity(final_qs[0])}"

        elif len(final_qs) > 1:
            output += ":\n  - "
            return output + "\n  - ".join([cls.format_quantity(q) for q in final_qs])

    @classmethod
    def format_errors(cls, *errors):
        unit_errors = [e for e in errors if isinstance(e, pint.UndefinedUnitError)]
        dim_errors = [e for e in errors if isinstance(e, pint.DimensionalityError)]
        error_strings = []

        if unit_errors != []:
            invalid_units = [f"`{e.args[0]}`" for e in unit_errors]
            string = "I don't recognise these units: "
            string += ", ".join(invalid_units) + ". "
            string += f"Try checking the [list of valid units]({Const.units_link}) (units are case sensitive)."
            error_strings.append(string)

        if dim_errors != []:
            string = f"I cant convert between: `\"{cls.format_unit(dim_errors[0].units1)}\" "\
            f"{cls.format_dim(dim_errors[0].dim1)}` and "
            string += ", ".join(
                [f"`\"{cls.format_unit(e.units2)}\" {cls.format_dim(e.dim2)}`" for e in dim_errors]
            )
            error_strings.append(string)

        return "\n\n".join(error_strings)


def add_currency_ureg(initial=True):
    res = requests.get("https://api.exchangeratesapi.io/latest?base=EUR").json()
    base = res["base"]
    # create base unit (can be anything)
    if initial:
        ureg.define(f"{base} = [currency]")
    currency_context = pint.Context("FX") # create context
    for currency,rate in res["rates"].items():
        if currency != base:
            ureg.define(f"{currency} = nan {base}")
            currency_context.redefine(f"{currency} = {1/rate} {base}") # add exchange rate to context
    ureg.add_context(currency_context) # add and enable context
    ureg.enable_contexts("FX")


def get_mentions():
    mentions = []
    for mention in reddit.inbox.mentions(limit=50):
        if mention.new:
            mentions.append(mention)
    for message in reddit.inbox.unread():
        if message.subject == "comment reply" or message.subject == "post reply":
            if Const.bot_name in message.body:
                mentions.append(message)
            else:
                message.mark_read()
        if Const.bot_name not in message.body:
            message.mark_read()
    return mentions


if __name__ in '__main__':
    config = configparser.ConfigParser()
    config.read("credentials.ini")
    credentials = config["Credentials"]

    ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
    add_currency_ureg() # can take longer on a poor connection

    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        username=credentials["username"],
        password=credentials["password"],
        user_agent="u/unit-convert",
    )

    for mention in get_mentions():
        Reply(mention, ureg, debug=True)


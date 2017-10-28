#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Catia
# Copyright 2014-2017 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# Catia é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""Main database with redis.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
__author__ = 'carlo'
from uuid import uuid1
import os
import redis


class Banco:
    def __init__(self):

        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        self.banco = redis.from_url(redis_url,  decode_responses=True)

    def __setitem__(self, key, value):
        self.banco.rpush(key, value)

    def __getitem__(self, key):
        banco = self.banco

        class Redis:
            def __init__(self, redis_):
                self._redis = redis_

            @staticmethod
            def append(data):
                banco.rpush(key, data)

            def __eq__(self, other):
                return self._redis == other

            @property
            def value(self):
                return self._redis

            @staticmethod
            def all():
                return banco.lrange(key, 0, -1)

        return Redis(self.banco.lrange(key, 0, -1))

    def delete(self, *args):
        self.banco.delete(*args)

    def save(self, value):
        key = str(uuid1())
        self.banco.rpush(key, value)
        return key


import unittest


class BancoTest(unittest.TestCase):
    def setUp(self):
        self.banco = Banco()

    def test_esquerda(self):
        """Cena esquerda vai é chamado."""
        self.banco.delete(1, 2)
        b = self.banco
        b[1] = '2'
        assert b[1].value == ['2'], "falhou em recuperar b[1]: %s" % str(b[1].value)
        b[1] = "[1:3]"
        assert b[1].value == ['2', "[1:3]"], "falhou em recuperar b[1]: %s" % str(b[1].value)
        c = b.save("{c:d}")
        assert b[c] == ["{c:d}"], "falhou em recuperar b[1]: %s" % str(b[c].value)
        b[c].append("[a:b]")
        assert b[c].all() == ["{c:d}", "[a:b]"], "falhou em recuperar b[c]: %s" % str(b[c].all()) + str(c)
        self.banco.banco.lrem(c, 0)
        b[c] = ""
        self.banco.delete(1, 2, c)


if __name__ == "__main__":
    unittest.main()
else:
    DRECORD = Banco()

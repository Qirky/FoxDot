""" Tests for BufferManager """
import os
import shutil
import tempfile
import unittest
from os.path import join

from FoxDot.lib.Buffers import BufferManager


class TestSampleSearch(unittest.TestCase):

    """ Test search functionality for sample files """
    def setUp(self):
        super(TestSampleSearch, self).setUp()
        def mkdir(dirname):
            os.mkdir(join(self.wd, dirname))
        def touch(filename):
            fullpath = join(self.wd, filename)
            open(fullpath, 'w').close()
            return fullpath
        self.wd = tempfile.mkdtemp()
        self.bm = BufferManager()
        self.bm._paths = [self.wd]
        self._yeah = touch('yeah.wav')
        mkdir('snares')
        self._snare1 = touch('snares/snare1.wav')
        self._snare2 = touch('snares/snare2.wav')
        mkdir('kicks')
        self._808 = touch('kicks/808.wav')
        self._kick = touch('kicks/kick.wav')
        mkdir('kicks/house')
        self._housekick = touch('kicks/house/house_bass.wav')

    def tearDown(self):
        super(TestSampleSearch, self).tearDown()
        shutil.rmtree(self.wd)

    def test_abspath(self):
        """ Sample file as absolute path """
        sample = join(self.wd, 'yeah.wav')
        found = self.bm._findSample(sample)
        self.assertEqual(found, sample)

    def test_abspath_no_ext(self):
        """ Sample file as absolute path with no extension """
        sample = join(self.wd, 'yeah')
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._yeah)

    def test_relpath(self):
        """ Sample file as relative path """
        sample = 'yeah.wav'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._yeah)

    def test_relpath_no_ext(self):
        """ Sample file as relative path with no extension """
        sample = 'yeah'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._yeah)

    def test_dir_first(self):
        """ Sample directory load first sample """
        sample = 'snares'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._snare1)

    def test_dir_nth(self):
        """ Sample directory load nth sample """
        sample = 'snares'
        found = self.bm._findSample(sample, 1)
        self.assertEqual(found, self._snare2)

    def test_dir_nth_overflow(self):
        """ Sample directory load nth sample (exceeds count) """
        sample = 'snares'
        found = self.bm._findSample(sample, 2)
        self.assertEqual(found, self._snare1)

    def test_nested_filename(self):
        """ Sample filename loaded from nested dir """
        sample = 'snare1.wav'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._snare1)

    def test_nested_filename_no_ext(self):
        """ Sample filename with no extension loaded from nested dir """
        sample = 'snare1'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._snare1)

    def test_pathpattern(self):
        """ Sample specified as pattern with path elements """
        sample = 'k?c*/*'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._808)

    def test_pathpattern_doublestar(self):
        """ Sample specified as pattern containing /**/ """
        sample = '**/snare*'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._snare1)

    def test_doublestar_deep_path(self):
        """ Sample specified as pattern containing /**/path """
        sample = '**/house/*'
        found = self.bm._findSample(sample)
        self.assertEqual(found, self._housekick)

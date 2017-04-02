from django.test import TestCase
from model_mommy import mommy
from django.utils.timezone import datetime
from smartsupport.models import Record #, Genre, Band, Music, Playlist

class TestRecord(TestCase):
  
  def setUp(self):
      self.record = mommy.make(Record, name='Sony Music')
      
  def test_record_creation(self):
      self.assertTrue(isinstance(self.record, Record))
      self.assertEquals(self.record.__str__(), self.record.name)

class TestGenre(TestCase):
  
  def setUp(self):
        self.genre = mommy.make(Genre, name='Rock')
      
  def test_genre_creation(self):
        self.assertTrue(isinstance(self.genre, Genre))
        self.assertEquals(self.genre.__str__(), self.genre.name)
        
        
class TestBand(TestCase):
  
  def setUp(self):
        self.record = mommy.make(Record, name='Sony Music')
        self.genre = mommy.make(Genre, name='Rock')
        self.band = mommy.make(Band, name='Twenty One Pilots', record=self.record, genre=self.genre)
        
  def test_band_creation(self):
        self.assertTrue(isinstance(self.band, Band))
        self.assertEquals(self.band.__str__(), self.band.name)
        
        
class TestMusic(TestCase):
  
  def setUp(self):
        self.record = mommy.make(Record, name='Sony Music')
        self.genre = mommy.make(Genre, name='Rock')
        self.band = mommy.make(Band, name='Twenty One Pilots', record=self.record, genre=self.genre)
        self.music = mommy.make(Music, name='Stress Out', band=self.band, duration=datetime.now(), year=datetime.now())
        
  def test_music_creation(self):
        self.assertTrue(isinstance(self.music, Music))
        self.assertEquals(self.music.__str__(), self.music.name)
        
        
class TestPlaylist(TestCase):
  
  def setUp(self):
        self.record = mommy.make(Record, name='Sony Music')
        self.genre = mommy.make(Genre, name='Rock')
        self.band = mommy.make(Band, name='Twenty One Pilots', record=self.record, genre=self.genre)
        self.music1 = mommy.make(Music, name='Stress Out', band=self.band, duration=datetime.now(), year=datetime.now())
        self.music2 = mommy.make(Music, name='Ride', band=self.band, duration=datetime.now(), year=datetime.now())
        self.smartsupport = mommy.make(Smartsupport, name='Rockerizando', music=[self.music1, self.music2])
        
  def test_playlist_creation(self):
        self.assertTrue(isinstance(self.smartsupport, Smartsupport))
        self.assertEquals(self.smartsupport.__str__(), self.smartsupport.name)
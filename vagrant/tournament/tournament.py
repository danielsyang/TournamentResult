#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

INSERT_PLAYER = "INSERT INTO player (name) values (%s)"
DELETE_ALL_PLAYER = "DELETE FROM player"
COUNT_PLAYER = "SELECT COUNT(*) FROM player"
INSERT_MATCH = "INSERT INTO MATCHES (winner, loser) values (%s, %s)"
DELETE_ALL_MATCHES = "DELETE FROM matches"

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(DELETE_ALL_MATCHES)
    conn.commit()

    cursor.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(DELETE_ALL_PLAYER)
    conn.commit()

    cursor.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(COUNT_PLAYER)
    result_count = cursor.fetchall()[0][0]

    cursor.close()
    conn.close()
    return result_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(INSERT_PLAYER, (name,))
    conn.commit()

    cursor.close()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(INSERT_MATCH, (winner,loser,))
    conn.commit()

    cursor.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

if __name__ == '__main__':
    deletePlayers();

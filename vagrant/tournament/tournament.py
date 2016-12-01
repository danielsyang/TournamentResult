#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

DATABASE_NAME = "tournament"
INSERT_PLAYER = "INSERT INTO players (name) values (%s)"
DELETE_ALL_PLAYERS = "TRUNCATE players CASCADE"
COUNT_PLAYER = "SELECT COUNT(*) FROM players"
INSERT_MATCH = "INSERT INTO MATCHES (winner, loser) values (%s, %s)"
DELETE_ALL_MATCHES = "TRUNCATE matches"

PLAYER_STANDINGS = ("SELECT  play.player_id AS p_id, play.name as name, "
                            "COALESCE(total_wins, 0) as total_wins, "
                            "COALESCE(total_matches, 0) as total_matches "
                            "FROM players play "
                            "LEFT JOIN total_matches tm "
                            "ON play.player_id = tm.player_id "
                            "LEFT JOIN total_wins tw "
                            "ON tm.player_id = tw.player_id "
                            "ORDER BY total_wins desc")


def connect():
    """Connect to the PostgreSQL database.
    Returns a database connection and a cursor."""
    try:
        db = psycopg2.connect("dbname={}".format(DATABASE_NAME))
        cursor = db.cursor()
        return db, cursor
    except:
        print "Failed to connect to database!"


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cursor = connect()
    cursor.execute(DELETE_ALL_MATCHES)
    conn.commit()

    cursor.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cursor = connect()
    cursor.execute(DELETE_ALL_PLAYERS)
    conn.commit()

    cursor.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cursor = connect()
    cursor.execute(COUNT_PLAYER)
    result_count = cursor.fetchone()[0]

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
    conn, cursor = connect()
    cursor.execute(INSERT_PLAYER, (name,))
    conn.commit()

    cursor.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cursor = connect()
    cursor.execute(PLAYER_STANDINGS)
    result_count = cursor.fetchall()

    cursor.close()
    conn.close()
    return result_count


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn, cursor = connect()
    cursor.execute(INSERT_MATCH, (winner, loser,))
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
    result = playerStandings()

    next_round_tup = []

    for i in range(0, len(result), 2):
        tup = (result[i][0], result[i][1], result[i+1][0], result[i+1][1])
        next_round_tup.append(tup)

    return next_round_tup


if __name__ == "__main__":
    print   swissPairings()

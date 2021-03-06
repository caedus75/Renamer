# Copyright (c) 2014 - 2018, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


#
# Exception
#
class MatchNotFoundError(Exception):
    '''Raise when show title, season or episodes can't be detected.'''


class SameFileError(Exception):
    '''Raise when current filename and new filename are the same.'''

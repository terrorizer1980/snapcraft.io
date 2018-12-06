import {
  PROMOTE_REVISION,
  UNDO_RELEASE,
  CANCEL_PENDING_RELEASES
} from "../actions/pendingReleases";

function removePendingRelease(state, revision, channel) {
  if (state[revision.revision]) {
    const channels = [...state[revision.revision].channels];

    if (channels.includes(channel)) {
      state = { ...state };
      channels.splice(channels.indexOf(channel), 1);
      state[revision.revision].channels = channels;
    }

    if (channels.length === 0) {
      state = { ...state };
      delete state[revision.revision];
    }
  }

  return state;
}

function promoteRevision(state = {}, revision, channel) {
  state = { ...state };

  // cancel any other pending release for the same channel in same architectures
  revision.architectures.forEach(arch => {
    Object.keys(state).forEach(revisionId => {
      const pendingRelease = state[revisionId];

      if (
        pendingRelease.channels.includes(channel) &&
        pendingRelease.revision.architectures.includes(arch)
      ) {
        state = removePendingRelease(state, pendingRelease.revision, channel);
      }
    });
  });

  // promote revision to channel
  let channels =
    state[revision.revision] && state[revision.revision].channels
      ? [...state[revision.revision].channels, channel]
      : [channel];

  // make sure channels are unique
  channels = channels.filter((item, i, ar) => ar.indexOf(item) === i);

  state[revision.revision] = {
    revision,
    channels
  };

  return state;
}
// revisions to be released:
// key is the id of revision to release
// value is object containing release object and channels to release to
// {
//  <revisionId>: {
//    revision: { revision: <revisionId>, version, ... },
//    channels: [ ... ]
//  }
// }
// TODO: remove `revision` from here, use only data from `revisions` state
// to prevent duplication of revison data
export default function pendingReleases(state = {}, action) {
  switch (action.type) {
    case PROMOTE_REVISION:
      return promoteRevision(
        state,
        action.payload.revision,
        action.payload.channel
      );
    case UNDO_RELEASE:
      return removePendingRelease(
        state,
        action.payload.revision,
        action.payload.channel
      );
    case CANCEL_PENDING_RELEASES:
      return {};
    default:
      return state;
  }
}

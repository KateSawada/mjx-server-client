#ifndef MJX_PROJECT_ACTION_H
#define MJX_PROJECT_ACTION_H

#include "mjx/internal/mjx.grpc.pb.h"

namespace mjx {
class Action {
 public:
  Action() = default;
  explicit Action(mjxproto::Action proto);
  explicit Action(const std::string& json);
  Action(int action_idx, const std::vector<Action>& legal_actions);
  bool operator==(const Action& other) const noexcept;
  bool operator!=(const Action& other) const noexcept;

  std::string ToJson() const noexcept;
  int ToIdx() const noexcept;  // 0 ~ 180

  // accessors
  const mjxproto::Action& proto() const noexcept;

 private:
  mjxproto::Action proto_{};
};
}  // namespace mjx

#endif  // MJX_PROJECT_ACTION_H
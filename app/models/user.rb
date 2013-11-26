class User < ActiveRecord::Base
  has_many :logs

  validates :username, presence: true
  validates_uniqueness_of :username, :case_sensitive => false
end


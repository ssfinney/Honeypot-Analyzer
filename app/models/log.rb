class Log < ActiveRecord::Base
  belongs_to :user, dependent: :destroy
  has_many :entries

  validates :name, presence: true
end

